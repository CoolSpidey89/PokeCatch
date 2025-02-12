from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext
import re
from shivu import application

async def check(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Check if the user has provided an ID to search for
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("❌ Please provide a valid character ID to check.")
        return

    character_id = context.args[0]

    # Query the database for the character by ID
    character = await db['anime_characters_lol'].find_one({"id": character_id})

    if character:
        # Format character details
        character_info = (
            f'🆔 <b>ID:</b> {character["id"]}\n'
            f'🆔 <b>Name:</b> {character["name"]}\n'
            f'🔹 <b>Category:</b> {character["category"]}\n'
            f'🎖 <b>Rarity:</b> {character["rarity"]}\n'
        )
        
        # Check if the img_url exists
        img_url = character.get("img_url", None)
        if img_url:
            # Send the character image with its details as caption
            await update.message.reply_photo(
                photo=img_url,
                caption=character_info,
                parse_mode="HTML"
            )
        else:
            # Send only text if no image is available
            await update.message.reply_text(character_info, parse_mode="HTML")
    else:
        await update.message.reply_text("❌ Character not found. Please check the ID and try again.")

# Add handler for /check command
application.add_handler(CommandHandler("check", check))
