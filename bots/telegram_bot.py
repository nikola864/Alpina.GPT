import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from django.conf import settings

# Глобальный словарь состояний пользователей
user_states = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context):
    """Обработчик команды /start"""
    chat_id = update.effective_chat.id
    token = context.args[0] if context.args else None

    if not token:
        await update.message.reply_text("Привет! Передайте токен бота: /start <токен>")
        return  # ← OK, потому что мы использовали await

    # Пример: просто подтверждение
    await update.message.reply_text(f"Добро пожаловать! Токен: {token}")
    user_states[chat_id] = {'token': token}


async def handle_message(update: Update, context):
    """Обработчик обычных сообщений"""
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_states:
        await update.message.reply_text("Начните с /start <токен>")
        return

    reply = f"Вы написали: {text}"
    await update.message.reply_text(reply)


def run_telegram_bot():
    """Функция для запуска бота в отдельном потоке"""
    logger.info("🚀 Запуск Telegram-бота...")

    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Telegram-бот запущен и работает")
    app.run_polling()