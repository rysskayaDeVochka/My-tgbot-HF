import os
import requests
from flask import Flask
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен и ID администратора
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "123456789"))  # Замени на свой ID

bot = Bot(BOT_TOKEN)
app = Flask(__name__)

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Напиши сообщение, начинающееся с #отправить")

# Обработчик обычных сообщений
def handle_message(update: Update, context: CallbackContext):
    if update.message.text.startswith("#отправить"):
        text = update.message.text.replace("#отправить", "").strip()
        bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
        update.message.reply_text("Сообщение отправлено администратору.")
    else:
        update.message.reply_text("Чтобы отправить админу, начни с #отправить.")

# Проверка доступности сайта
@app.route('/')
def index():
    return "Бот работает на polling!"

# Запуск бота
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    from threading import Thread
    Thread(target=main).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
