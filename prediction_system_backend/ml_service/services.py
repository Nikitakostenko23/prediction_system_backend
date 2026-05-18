from dataclasses import asdict
from urllib.parse import urljoin

import requests
from celery import current_app
from django.conf import settings
from rest_framework.status import is_success

from cabinet.dataclasses import MedicalCardData
from cabinet.models import PredictionRun, Prediction, ComplicationGroup
from ml_service.constants import VALUE_TO_CONSIDER_COMPLICATIONS_PRESENCE
from ml_service.dataclasses import PredictionData, MultiClassPredictionData
from ml_service.exceptions import PredictionRunException
from ml_service.models import MlModel


class PredictionInterface:
    """Интерфейс запуска прогнозирования"""

    MULTI_LABEL_BY_BINARY_MODEL = {
        'cas': 'cas_multi_label',
        'cee_classic': 'cee_classic_multi_label',
        'cee_eversional': 'cee_eversional_multi_label',
    }

    def __init__(self, prediction_run: PredictionRun):
        self.predictions_to_create: list[Prediction] = []
        self.prediction_run: PredictionRun = prediction_run
        self.multi_label_ml_model_slugs_to_run: set[str] = set()

    def cancel_prediction_run(self):
        """Отменить прогнозирование"""
        current_app.control.revoke(self.prediction_run.task_id, terminate=True)
        self._change_prediction_run_state(status=PredictionRun.CANCELED)

    def run_prediction(self, medical_card_data: MedicalCardData) -> None:
        """
        Запустить прогнозирование.
        Функция последовательно ходит на сервис машинного обучения, передавая данные из медкарты и слаг модели
        Порядок вызова моделей:
        1) КАС (бинарная)
        2) КЭЭ классическая (бинарная)
        3) КЭЭ эверсионная (бинарная)
        4) КЭЭ гломуссохраняющая (бинарная)
        5) КАС (многометочная, если бинарная показала, что есть осложнение)
        6) КЭЭ классическая (многометочная, если есть осложнение)
        7) КЭЭ эверсионная (многометочная, если есть осложнение)
        """
        try:
            self._change_prediction_run_state(status=PredictionRun.IN_PROGRESS)
            self._run_binary_prediction(medical_card_data)
            self._run_multi_label_prediction(medical_card_data)
            Prediction.objects.bulk_create(self.predictions_to_create, batch_size=100)
            self._finalize_prediction_run()
            self._change_prediction_run_state(status=PredictionRun.SUCCESS)
        except Exception as error:
            self._change_prediction_run_state(status=PredictionRun.FAILED)
            raise error

    def _change_prediction_run_state(self, *, status: str) -> None:
        """Изменить статус объекта запуска прогнозирования"""
        self.prediction_run.status = status
        self.prediction_run.save(update_fields=['status', 'updated_at'])

    def _finalize_prediction_run(self):
        """Дозаполнить данными запуск прогнозирования"""
        lowest_prediction = (
            Prediction.objects.filter(prediction_run=self.prediction_run)
            .order_by('probability')
            .first()
        )
        self.prediction_run.summary_probability = lowest_prediction.probability
        self.prediction_run.stenting_type = lowest_prediction.stenting_type
        self.prediction_run.save(
            update_fields=[
                'summary_probability',
                'stenting_type',
                'updated_at',
            ],
        )

    @staticmethod
    def _send_request(
        *,
        model_slug: str,
        prediction_type: str,
        medical_card_data: MedicalCardData,
        complication_group_slugs: list[str] | None = None,
    ) -> PredictionData | MultiClassPredictionData:
        """Отправить запрос на сервис машинного обучения"""
        response = requests.post(
            urljoin(settings.ML_SERVICE_URL, f'/predict/{prediction_type}/'),
            json={
                'ml_model_slug': model_slug,
                'medical_card': asdict(medical_card_data),
                'complication_group_slugs': complication_group_slugs,
            },
            timeout=60,
        )
        if not is_success(response.status_code):
            raise PredictionRunException(f'{response.status_code}')

        return response.json()

    def _run_binary_prediction(self, medical_card_data: MedicalCardData):
        """Запустить бинарную классификацию"""
        binary_classification_models = MlModel.objects.filter(type=MlModel.BINARY_CLASSIFICATION).order_by('order')
        for binary_classification_model in binary_classification_models:
            data: PredictionData = self._send_request(
                model_slug=binary_classification_model.slug,
                prediction_type=binary_classification_model.type,
                medical_card_data=medical_card_data,
            )
            multi_label_ml_model_slug = self.MULTI_LABEL_BY_BINARY_MODEL.get(binary_classification_model.slug)
            if (
                multi_label_ml_model_slug
                and data['probability'] >= VALUE_TO_CONSIDER_COMPLICATIONS_PRESENCE
            ):
                self.multi_label_ml_model_slugs_to_run.add(multi_label_ml_model_slug)

            self.predictions_to_create.append(
                Prediction(
                    probability=data['probability'],
                    stenting_type=binary_classification_model.stenting_type,
                    prediction_run=self.prediction_run,
                    complication_group=None,
                    ml_model=binary_classification_model,
                )
            )

    def _run_multi_label_prediction(self, medical_card_data: MedicalCardData):
        """Запустить многометочную классификацию"""
        multi_label_classification_models = MlModel.objects.filter(
            type=MlModel.MULTI_LABEL_CLASSIFICATION,
            slug__in=self.multi_label_ml_model_slugs_to_run,
        ).order_by('order')
        complication_group_by_slug = ComplicationGroup.objects.all().in_bulk(field_name='slug')
        for multi_label_classification_model in multi_label_classification_models:
            data = self._send_request(
                model_slug=multi_label_classification_model.slug,
                prediction_type=multi_label_classification_model.type,
                medical_card_data=medical_card_data,
                complication_group_slugs=list(complication_group_by_slug),
            )
            for complication_group_slug, probability in data['probability_by_group_slug'].items():
                self.predictions_to_create.append(
                    Prediction(
                        probability=probability,
                        stenting_type=multi_label_classification_model.stenting_type,
                        prediction_run=self.prediction_run,
                        complication_group=complication_group_by_slug[complication_group_slug],
                        ml_model=multi_label_classification_model,
                    )
                )
