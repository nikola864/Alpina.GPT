from rest_framework import viewsets
from .models import Scenario, Step
from .serializers import ScenarioSerializer, StepSerializer

class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

class StepViewSet(viewsets.ModelViewSet):
    serializer_class = StepSerializer

    def get_queryset(self):
        scenario_id = self.kwargs.get('scenario_pk')
        if scenario_id:
            return Step.objects.filter(scenario_id=scenario_id)
        return Step.objects.none()

