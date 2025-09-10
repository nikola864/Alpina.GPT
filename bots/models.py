from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    name = models.CharField('Название бота', max_length=100)
    description = models.TextField('Описание', blank=True)
    telegram_token = models.CharField('Токен telegram', max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    created_ad = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = "Боты"


class Scenario(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='scenarios', verbose_name="Бот")
    name = models.CharField("Название сценария", max_length=100)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.bot.name})"

    class Meta:
        verbose_name = "Сценарий"
        verbose_name_plural = "Сценарии"


class Step(models.Model):
    class Step(models.Model):
        STEP_TYPE_CHOICES = [
            ('prompt', 'Запрос к GPT'),
            ('message', 'Текстовое сообщение'),
            ('input', 'Ожидание ввода'),
        ]

        scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='steps', verbose_name="Сценарий")
        name = models.CharField("Название шага", max_length=100)
        step_type = models.CharField("Тип шага", max_length=20, choices=STEP_TYPE_CHOICES, default='prompt')
        prompt_text = models.TextField("Промпт для GPT", blank=True, help_text="Текст, который отправляется в GPT")
        response_text = models.TextField("Фиксированный ответ", blank=True, help_text="Если тип message")
        condition = models.JSONField("Условия перехода", blank=True, null=True,
                                     help_text='{"next_step_id": 5, "if": "contains", "value": "да"}')
        order = models.PositiveIntegerField("Порядок", default=1)

        class Meta:
            ordering = ['order']
            verbose_name = "Шаг"
            verbose_name_plural = "Шаги"

        def __str__(self):
            return f"{self.name} ({self.scenario.name})"







