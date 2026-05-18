from django.contrib import admin

from ml_service.models import MlModel, MlModelMetric


@admin.register(MlModel)
class MlModelAdmin(admin.ModelAdmin):
    """Админ для модели MLModel"""

    list_display = ['name', 'slug', 'type', 'preprocessing_method', 'stenting_type']
    search_fields = ['name', 'slug', 'type']
    list_filter = ['type']


@admin.register(MlModelMetric)
class MlModelMetricAdmin(admin.ModelAdmin):
    """Админ для модели MlModelMetric"""

    list_display = [
        'ml_model',
        'accuracy',
        'recall',
        'precision',
        'f1_score',
        'roc_auc',
        'phase',
        'dataset_version',
    ]
    list_filter = ['ml_model']
