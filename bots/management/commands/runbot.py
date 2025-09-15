import os
import django
from django.core.management.base import BaseCommand

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alpina_GPT.settings')
django.setup()

# Теперь можно импортировать модели
from bots.telegram_bot import run_telegram_bot


class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Запуск Telegram бота...")
        run_telegram_bot()