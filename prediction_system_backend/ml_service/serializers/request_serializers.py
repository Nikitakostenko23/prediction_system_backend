from rest_framework import serializers


class OcclusionTimeRequestSerializer(serializers.Serializer):
    """Сериализатор запроса на изменение времени окклюзии"""

    occlusion_time = serializers.IntegerField(help_text='Время окклюзии', min_value=0)
