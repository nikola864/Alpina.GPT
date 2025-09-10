from django.contrib import admin
from .models import Bot, Scenario, Step

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name', 'bot', 'created_at')
    list_filter = ('bot',)
    search_fields = ('name',)

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('name', 'scenario', 'step_type', 'order')
    list_filter = ('step_type', 'scenario')