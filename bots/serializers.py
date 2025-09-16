from rest_framework import serializers
from .models import Bot
from scenarios.models import Scenario  # ← добавил импорт модели
from scenarios.serializers import ScenarioSerializer


class BotSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer(read_only=True)
    scenario_id = serializers.PrimaryKeyRelatedField(
        queryset=Scenario.objects.all(),  # ← теперь работает!
        source='scenario',
        write_only=True,
        required=True,
        allow_null=True,
    )

    class Meta:
        model = Bot
        fields = '__all__'