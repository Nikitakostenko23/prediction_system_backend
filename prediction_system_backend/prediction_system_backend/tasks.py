from celery import shared_task

from cabinet.dataclasses import MedicalCardData
from cabinet.models import PredictionRun
from ml_service.services import PredictionInterface


@shared_task
def task_run_prediction(prediction_run_id, medical_card_data: dict[str, str | bool]):
    """Запустить прогнозирование"""
    prediction_run = PredictionRun.objects.get(id=prediction_run_id)
    PredictionInterface(prediction_run).run_prediction(MedicalCardData(**medical_card_data))
