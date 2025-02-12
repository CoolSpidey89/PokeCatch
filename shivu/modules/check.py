from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext
import re
from shivu import application

async def check_pokemon(update: Update, context: CallbackContext) -> None:
    """Fetches Pokémon details from the database using an ID."""
    
    if not context.args:
        await update.message.reply_text("❌ Please provide a Pokémon ID. Example: `/check 123`", parse_mode="Markdown")
        return
    
    pokemon_id = context.args[0]

    # ✅ Validate ID (only allow numbers)
    if not re.match(r"^\d+$", pokemon_id):
        await update.message.reply_text("❌ Invalid ID! Use numbers only. Example: `/check 123`", parse_mode="Markdown")
        return

    # ✅ Fetch Pokémon from the database
    pokemon = await collection.find_one({"id": pokemon_id})

    if not pokemon:
        await update.message.reply_text("❌ No Pokémon found with this ID!", parse_mode="Markdown")
        return

    # ✅ Extract Pokémon details
    name = pokemon.get("name", "Unknown")
    category = pokemon.get("category", "Unknown")
    rarity = pokemon.get("rarity", "Unknown")
    img_url = pokemon.get("img_url", None)

    # ✅ Format the message
    message = (
        f"📜 **Pokémon Details**\n"
        f"🆔 **ID:** `{pokemon_id}`\n"
        f"🔹 **Name:** {name}\n"
        f"🌟 **Category:** {category}\n"
        f"🎖 **Rarity:** {rarity}\n"
    )

    # ✅ Include image if available
    if img_url:
        await update.message.reply_photo(photo=img_url, caption=message, parse_mode="Markdown")
    else:
        await update.message.reply_text(message, parse_mode="Markdown")


# ✅ Add the command handler to your bot
application.add_handler(CommandHandler("check", check_pokemon, block=False))
