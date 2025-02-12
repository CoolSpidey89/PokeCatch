import time

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

async def ping(update: Update, context: CallbackContext) -> None:
    logger.info(f"Received ping command from {update.effective_user.id}")
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text("Nouu.. it's Sudo user's Command..")
        return

    start_time = time.time()
    message = await update.message.reply_text('Pong!')
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    await message.edit_text(f'Pong! {elapsed_time}ms')

application.add_handler(CommandHandler("ping", ping))
