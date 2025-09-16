import os
import django
from django.core.management.base import BaseCommand
from threading import Thread


class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        # Настройка Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()

        self.stdout.write("🌍 Django настроен...")

        # Теперь импортируем после setup()
        from bots.telegram_bot import run_telegram_bot

        self.stdout.write("🤖 Запуск Telegram-бота в фоновом потоке...")

        # Запускаем бота в отдельном потоке
        bot_thread = Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()

        self.stdout.write(
            self.style.SUCCESS("✅ Команда 'runbot' запущена. Бот работает в фоне.")
        )

        # Чтобы скрипт не завершался
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.stdout.write("👋 Остановка бота...")