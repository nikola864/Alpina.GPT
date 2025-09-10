from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bot, Scenario, Step
from .serializers import BotSerializer, ScenarioSerializer, ScenarioDetailSerializer, StepSerializer

class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    @action(detail=True, methods=['get'])
    def scenarios(self, request, pk=None):
        bot = self.get_object()
        scenarios = bot.scenarios.all()
        serializer = ScenarioSerializer(scenarios, many=True)
        return Response(serializer.data)


class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScenarioDetailSerializer
        return ScenarioSerializer

    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        scenario = self.get_object()
        steps = scenario.steps.all().order_by('order')
        serializer = StepSerializer(steps, many=True)
        return Response(serializer.data)


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

    def get_queryset(self):
        scenario_id = self.kwargs.get('scenario_id')
        if scenario_id:
            return Step.objects.filter(scenario_id=scenario_id)
        return Step.objects.all()