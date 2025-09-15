from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bots.views import BotViewSet
from scenarios.views import ScenarioViewSet, StepViewSet

router = DefaultRouter()
router.register(r'bots', BotViewSet)
router.register(r'scenarios', ScenarioViewSet)
router.register(r'scenarios/(?P<scenario_pk>[^/.]+)/steps', StepViewSet, basename='scenario-steps')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
