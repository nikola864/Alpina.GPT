import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from .models import Bot as BotModel
from .gpt_service import generate_response
from django.conf import settings

logging.basicConfig(level=logging.INFO)

# Храним состояние пользователей: {chat_id: {'bot_id': ..., 'current_step': ...}}
user_states = {}


async def start(update: Update, context):
    chat_id = update.effective_chat.id
    token = context.args[0] if context.args else None

    if not token:
        await update.message.reply_text("Привет! Передайте токен бота: /start <токен>")
        return

    try:
        bot = BotModel.objects.get(telegram_token=token)
        user_states[chat_id] = {
            'bot_id': bot.id,
            'current_scenario_id': bot.scenario.id if bot.scenario else None,
            'current_step_id': None,
            'dialog_history': []  # для контекста GPT
        }
        await update.message.reply_text(f"Добро пожаловать в {bot.name}!")
    except BotModel.DoesNotExist:
        await update.message.reply_text("Бот с таким токеном не найден.")


async def handle_message(update: Update, context):
    chat_id = update.effective_chat.id
    text = update.message.text

    state = user_states.get(chat_id)
    if not state:
        await update.message.reply_text("Начните с /start <токен>")
        return

    bot = BotModel.objects.get(id=state['bot_id'])
    scenario = bot.scenario

    if not scenario:
        reply = generate_response(text, state.get('dialog_history', []))
        state['dialog_history'].append((text, reply))
        await update.message.reply_text(reply)
        return

    # Логика сценария
    current_step_id = state.get('current_step_id')

    if not current_step_id:
        first_step = scenario.steps.order_by('id').first()
        if not first_step:
            await update.message.reply_text("Сценарий пуст.")
            return
        current_step_id = first_step.step_id
        state['current_step_id'] = current_step_id

    step = scenario.steps.get(step_id=current_step_id)

    if step.step_type == 'gpt':
        reply = generate_response(text, state.get('dialog_history', []))
        state['dialog_history'].append((text, reply))
        await update.message.reply_text(reply)
    elif step.step_type == 'text':
        await update.message.reply_text(step.content)
    elif step.step_type == 'question':
        await update.message.reply_text(step.content)
    elif step.step_type == 'end':
        await update.message.reply_text(step.content or "Диалог завершён.")
        del user_states[chat_id]
        return

    # Переход к следующему шагу
    if step.next_step_id:
        state['current_step_id'] = step.next_step_id
    else:
        # Если нет следующего — заканчиваем
        await update.message.reply_text("Сценарий завершён.")
        del user_states[chat_id]


def run_telegram_bot():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()