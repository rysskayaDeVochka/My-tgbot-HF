import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_GROUP_ID = int(os.getenv('ADMIN_GROUP_ID'))

async def relay_private(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    header = f"Сообщение от пользователя {msg.from_user.id}:"
    if msg.text:
        await ctx.bot.send_message(chat_id=ADMIN_GROUP_ID, text=f"{header}\n{msg.text}")
    if msg.photo:
        await ctx.bot.send_photo(chat_id=ADMIN_GROUP_ID, photo=msg.photo[-1].file_id, caption=header)

async def relay_group(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg.chat.id != ADMIN_GROUP_ID:
        return

    if not msg.reply_to_message or "#отправить" not in msg.text.lower():
        return

    reply = msg.reply_to_message
    match = re.search(r"Сообщение от пользователя (\d+):", reply.text)
    if not match:
        return

    target_id = int(match.group(1))
    clean_text = msg.text.replace("#отправить", "").strip()
    if clean_text:
        await ctx.bot.send_message(chat_id=target_id, text=clean_text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE, relay_private))
    app.add_handler(MessageHandler(filters.Chat(ADMIN_GROUP_ID) & filters.TEXT, relay_group))
    app.run_polling()

if __name__ == '__main__':
    main()
