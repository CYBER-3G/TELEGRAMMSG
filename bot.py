import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

admin_messages = set()

async def save_admin_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = update.message.message_id

    try:
        member = await context.bot.get_chat_member(chat_id, user_id)

        if member.status in ["administrator", "creator"]:
            admin_messages.add((chat_id, message_id))
    except:
        pass


async def delete_admin_messages(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, message_id in list(admin_messages):
        try:
            await context.bot.delete_message(chat_id, message_id)
        except:
            pass

    admin_messages.clear()


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, save_admin_messages))

    # every 10 minutes
    app.job_queue.run_repeating(delete_admin_messages, interval=600, first=600)

    print("Bot started...")

    await app.run_polling()


import asyncio
asyncio.run(main())
