#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line
import sys


if __name__ == '__main__':
    # Устанавливаем переменную окружения для настроек Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alpina_GPT.settings')

    # Запускаем настройку Django ДО любых импортов моделей
    django.setup()

    # Теперь можно обрабатывать команды
    if len(sys.argv) > 1:
        command = sys.argv[1]

        # Если команда — runbot, запускаем Telegram-бота
        if command == 'runbot':
            try:
                from bots.telegram_bot import run_telegram_bot
                run_telegram_bot()
            except Exception as e:
                print(f"Ошибка при запуске бота: {e}")
                raise
            sys.exit(0)

    # Все остальные команды (runserver, migrate и т.д.)
    execute_from_command_line(sys.argv)