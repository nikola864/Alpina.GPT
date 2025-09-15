from django.db import models

class Scenario(models.Model):
    title = models.CharField('Загаловок', max_length=100)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сценарий"
        verbose_name_plural = "Сценарии"

class Step(models.Model):
    STEP_TYPE_CHOICES = [
        ('text', 'Текст от бота'),
        ('question', 'Вопрос пользователю'),
        ('gpt', 'Генерация через GPT'),
        ('end', 'Конец сценария'),
    ]

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='steps')
    step_id = models.CharField('ID шага', max_length=50, help_text='Уникальный ID в рамках сценария, например step_1')
    title = models.CharField('Название шага', max_length=50, blank=True)
    content = models.TextField('Контент', blank=True, help_text='Текст или промпт для GPT')
    step_type = models.CharField('Тип шага', max_length=20, choices=STEP_TYPE_CHOICES, default='text')
    next_step_id = models.CharField('Следующий шаг', max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.scenario.title} — {self.step_id}"

    class Meta:
        unique_together = ['scenario', 'step_id']
        verbose_name = "Шаг сценария"
        verbose_name_plural = "Шаги сценария"















