from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, collection, user_collection  # ✅ Import application
import datetime, random


# Time limit for claiming (24 hours)
CLAIM_COOLDOWN_HOURS = 24

# Function to handle /claim command
async def claim(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # ✅ Fetch user data from database
    user = await user_collection.find_one({"id": user_id})

    # ✅ Check last claim time
    last_claim_time = user.get("last_claim", None) if user else None
    now = datetime.datetime.utcnow()

    if last_claim_time:
        last_claim_time = datetime.datetime.strptime(last_claim_time, "%Y-%m-%d %H:%M:%S")
        time_diff = (now - last_claim_time).total_seconds()

        if time_diff < (CLAIM_COOLDOWN_HOURS * 3600):
            remaining_time = datetime.timedelta(seconds=(CLAIM_COOLDOWN_HOURS * 3600 - time_diff))
            await update.message.reply_text(
                f"⏳ You have already claimed a Pokémon! Come back in {str(remaining_time).split('.')[0]}."
            )
            return

    # ✅ Get all available Pokémon characters (excluding restricted ones)
    RESTRICTED_RARITIES = ["🔮 Limited-Edition", "🌐 God"]
    all_characters = list(await collection.find({"rarity": {"$nin": RESTRICTED_RARITIES}}).to_list(length=None))

    if not all_characters:
        await update.message.reply_text("❌ No Pokémon cards available at the moment!")
        return

    # ✅ Select a random Pokémon character
    character = random.choice(all_characters)

    # ✅ Assign rewards based on rarity
    REWARD_TABLE = {
        "⚪ Common": (100, 150),
        "🟢 Uncommon": (150, 250),
        "🔵 Rare": (200, 350),
        "🟣 Extreme": (300, 450),
        "🟡 Sparking": (400, 600),
        "🔱 Ultra": (500, 800),
        "💠 Legends Limited": (750, 1200),
        "🔮 Zenkai": (800, 1300),
        "🏆 Event-Exclusive": (1000, 1500)
    }

    rarity = character.get("rarity", "⚪ Common")
    coins_min, coins_max = REWARD_TABLE.get(rarity, (100, 200))
    coins_won = random.randint(coins_min, coins_max)

    # ✅ Update user's database entry
    if user:
        await user_collection.update_one(
            {"id": user_id},
            {
                "$set": {"last_claim": now.strftime("%Y-%m-%d %H:%M:%S")},
                "$push": {"characters": character},
                "$inc": {"coins": coins_won}
            }
        )
    else:
        await user_collection.insert_one({
            "id": user_id,
            "username": update.effective_user.username,
            "first_name": update.effective_user.first_name,
            "characters": [character],
            "coins": coins_won,
            "last_claim": now.strftime("%Y-%m-%d %H:%M:%S")
        })

    # ✅ Create an inline button to view the user's collection
    keyboard = [[InlineKeyboardButton("See Collection", switch_inline_query_current_chat=f"collection.{user_id}")]]
    
    # ✅ Send success message with character details
    await update.message.reply_photo(
        photo=character.get("img_url", ""),
        caption=(
            f"🎉 <b>{update.effective_user.first_name}</b>, you have claimed a Pokémon!\n\n"
            f"🆔 <b>Name:</b> {character['name']}\n"
            f"🔹 <b>Category:</b> {character.get('category', 'Unknown')}\n"
            f"🎖 <b>Rarity:</b> {character.get('rarity', 'Common')}\n\n"
            f"💰 <b>Coins Earned:</b> {coins_won} 🪙\n\n"
            f"Use /collection to view all your Pokémon!"
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Add /claim command to bot
application.add_handler(CommandHandler("claim", claim, block=False))
