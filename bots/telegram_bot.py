import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from .gpt import get_gpt_response
from .models import Bot as BotModel, Scenario, Step

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на базе Alpina.GPT. Напиши что-нибудь!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    # Найдём бота по токену (упрощённо)
    try:
        bot = BotModel.objects.get(telegram_token=settings.TELEGRAM_BOT_TOKEN)
        scenario = bot.scenarios.first()  # Берём первый сценарий
        if not scenario:
            await update.message.reply_text("Сценарий не найден.")
            return

        step = scenario.steps.order_by('order').first()
        if step and step.step_type == 'prompt':
            prompt = step.prompt_text.format(user_message=user_message)
            reply = get_gpt_response(prompt)
        else:
            reply = "Спасибо за сообщение!"

        await update.message.reply_text(reply)
    except BotModel.DoesNotExist:
        await update.message.reply_text("Бот не настроен.")

def run_telegram_bot():
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # В режиме polling (для разработки)
    app.run_polling()