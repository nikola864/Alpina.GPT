from django.contrib import admin
from .models import Scenario, Step


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'step_id', 'step_type', 'title')
    list_filter = ('scenario', 'step_type')
    search_fields = ('step_id', 'content')

