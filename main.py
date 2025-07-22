import os
from flask import Flask, request
import telegram

TOKEN = "7207584353:AAGY8XRHOq0Ial6gn3_xqNrnRSWHCivp1es"
ADMIN_CHAT_ID = -1002879409912

bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bot is running."

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        if update.message.chat.type == "private":
            # Сообщение от пользователя → в админ-группу
            text = update.message.text or ""
            caption = update.message.caption or ""
            if update.message.photo:
                bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=update.message.photo[-1].file_id,
                               caption=f"От пользователя @{update.message.from_user.username or update.message.from_user.id}:\n{caption}")
            else:
                bot.send_message(chat_id=ADMIN_CHAT_ID,
                                 text=f"От пользователя @{update.message.from_user.username or update.message.from_user.id}:\n{text}")
        elif update.message.chat.id == ADMIN_CHAT_ID:
            if update.message.reply_to_message and "#отправить" in update.message.text.lower():
                # Ответ из группы → пользователю
                lines = update.message.reply_to_message.text.split('\n')
                for line in lines:
                    if line.startswith("От пользователя @"):
                        user_ref = line.split("От пользователя @")[1].split(":")[0]
                        break
                else:
                    return "User ID not found"

                # Попробуем отправить по username, если не получится — как ID
                text_to_send = update.message.text.replace("#отправить", "").strip()
                try:
                    bot.send_message(chat_id=f"@{user_ref}", text=text_to_send)
                except telegram.error.TelegramError:
                    try:
                        bot.send_message(chat_id=int(user_ref), text=text_to_send)
                    except Exception as e:
                        print("Error sending to user:", e)
    return "ok"
