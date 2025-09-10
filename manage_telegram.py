# run_telegram_bot.py

import os
import django
import logging

# Установи переменную окружения и настрой Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alpina_gpt.settings')
django.setup()  # <-- Это ключевая строка: загружает Django

# Теперь можно использовать models, settings и т.д.
from bots.telegram_bot import run_telegram_bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_telegram_bot()