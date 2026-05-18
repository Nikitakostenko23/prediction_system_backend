from django.db import models

from common_utils.mixins import AutoDateMixin


class MlModel(AutoDateMixin):
    """Модель машинного обучения"""

    BINARY_CLASSIFICATION = 'binary'
    MULTI_LABEL_CLASSIFICATION = 'multi_label'
    ML_MODEL_CHOICES = {
        BINARY_CLASSIFICATION: 'Бинарная классфикация',
        MULTI_LABEL_CLASSIFICATION: 'Многометочная классификация',
    }

    name = models.CharField('Название', unique=True, max_length=100)
    slug = models.SlugField('Слаг', unique=True, max_length=100)
    type = models.CharField('Тип', choices=ML_MODEL_CHOICES, max_length=50)
    preprocessing_method = models.CharField(
        'Метод предобработки данных', max_length=100
    )
    description = models.CharField('Описание', max_length=1000)
    stenting_type = models.ForeignKey(
        'cabinet.StentingType',
        verbose_name='Тип стентирования',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField('Порядок выполнения', unique=True)

    class Meta:
        verbose_name = 'Модель машинного обучения'
        verbose_name_plural = 'Модели машинного обучения'
        ordering = ('order',)

    def __str__(self):
        return self.name


class MlModelMetric(AutoDateMixin):
    """Метрика модели машинного обучения"""

    accuracy = models.DecimalField('Достоверность', max_digits=5, decimal_places=2)
    recall = models.DecimalField('Полнота', max_digits=5, decimal_places=2)
    precision = models.DecimalField('Точность', max_digits=5, decimal_places=2)
    f1_score = models.DecimalField('Ф1', max_digits=5, decimal_places=2)
    roc_auc = models.DecimalField(
        'Отношение под ROC-кривой к площади идеального квадрата',
        max_digits=5,
        decimal_places=2,
    )
    phase = models.CharField('Фаза', max_length=20)
    dataset_version = models.CharField('Версия датасета', max_length=20)
    ml_model = models.ForeignKey(
        MlModel, verbose_name='Модель машинного обучения', on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Метрика модели машинного обучения'
        verbose_name_plural = 'Метрики машинного обучения'
        ordering = (
            '-created_at',
            '-dataset_version',
        )

    def __str__(self):
        return f'{self.ml_model} {self.dataset_version} | {self.phase}'
