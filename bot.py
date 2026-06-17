import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8930787917:AAGo5QSTThLWpMW0kT5KIKd4StIwOOQPSjE")
ADMIN_USERNAME = "soloveyco"

NAME, LEVEL, SOURCE = range(3)

LEVELS = [["A1 — начинающий", "A2 — elementary"],
          ["B1 — intermediate", "B2 — upper intermediate"],
          ["C1 — advanced", "C2 — почти носитель"]]

SOURCES = [["Instagram", "Telegram"],
           ["От друга / знакомого", "Сайт starspeaking.ru"],
           ["Другое"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! ✨\n\n"
        "Это запись на встречу StarSpeaking:\n\n"
        "🎮 *Game Night*\n"
        "📅 Четверг, 18 июня · 20:00 МСК\n"
        "🌐 Онлайн\n\n"
        "Давай запишем тебя! Как тебя зовут?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        f"Отлично, {update.message.text}! 🌟\n\nКакой у тебя уровень английского?",
        reply_markup=ReplyKeyboardMarkup(LEVELS, one_time_keyboard=True, resize_keyboard=True)
    )
    return LEVEL

async def get_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["level"] = update.message.text
    await update.message.reply_text(
        "Откуда ты узнал(а) о StarSpeaking?",
        reply_markup=ReplyKeyboardMarkup(SOURCES, one_time_keyboard=True, resize_keyboard=True)
    )
    return SOURCE

async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["source"] = update.message.text
    user = update.message.from_user

    name   = context.user_data["name"]
    level  = context.user_data["level"]
    source = context.user_data["source"]
    tg     = f"@{user.username}" if user.username else f"id:{user.id}"

    await update.message.reply_text(
        f"Ты записан(а)! 🎉\n\n"
        f"Ждём тебя в четверг 18 июня в 20:00 МСК на *Game Night* 🎮\n\n"
        f"Аня скоро напишет тебе со ссылкой на встречу. "
        f"Если есть вопросы — пиши сюда или в @soloveyco ✨",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

    await context.bot.send_message(
        chat_id=f"@{ADMIN_USERNAME}",
        text=(
            f"🌟 *Новая запись на Game Night 18 июня!*\n\n"
            f"👤 Имя: {name}\n"
            f"📊 Уровень: {level}\n"
            f"🔍 Откуда: {source}\n"
            f"✈️ Telegram: {tg}"
        ),
        parse_mode="Markdown"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Окей, запись отменена. Если передумаешь — просто напиши /start ✨",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LEVEL:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_level)],
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_source)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
