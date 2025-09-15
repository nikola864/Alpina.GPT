from django.db import models
from scenarios.models import Scenario

class Bot(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    telegram_token = models.CharField('Токен Telegram', max_length=100, unique=True)
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Сценарий по умолчанию',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Боты"


