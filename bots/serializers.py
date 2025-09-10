from rest_framework import serializers
from .models import Bot, Scenario, Step

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'

class StepListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'name', 'step_type', 'order']

class ScenarioSerializer(serializers.ModelSerializer):
    steps = StepListSerializer(many=True, read_only=True)

    class Meta:
        model = Scenario
        fields = '__all__'

class ScenarioDetailSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = Scenario
        fields = '__all__'

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        scenario = Scenario.objects.create(**validated_data)
        for step_data in steps_data:
            Step.objects.create(scenario=scenario, **step_data)
        return scenario

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Удаляем старые шаги
        instance.steps.all().delete()
        for step_data in steps_data:
            Step.objects.create(scenario=instance, **step_data)

        return instance

class BotSerializer(serializers.ModelSerializer):
    scenarios_count = serializers.SerializerMethodField()

    class Meta:
        model = Bot
        fields = '__all__'

    def get_scenarios_count(self, obj):
        return obj.scenarios.count()