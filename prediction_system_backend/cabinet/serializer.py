from rest_framework import serializers

from cabinet.models import PredictionRun, StentingType


class PredictionRunFilterSerializer(serializers.Serializer):
    """Сериализатор фильтров"""

    status = serializers.ChoiceField(label='Статус', choices=PredictionRun.STATUS_CHOICES, required=False)
    stenting_type_id = serializers.CharField(label='Id типа стентирования', required=False)
    date_start = serializers.DateField(label='Дата начала', required=False)
    date_end = serializers.DateField(label='Дата окончания', required=False)
