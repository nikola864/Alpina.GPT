#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alpina_GPT.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

OPENAI_API_KEY = 'sk-ваш-ключ-здесь'  # Замени на настоящий
TELEGRAM_BOT_TOKEN = '8493795627:AAHy_gdXtI1ekcYtN64Ydj9SXnQ0UbFa1vQ'  # Твой токен от BotFather

if __name__ == '__main__':
    main()

