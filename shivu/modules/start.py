import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from shivu import pm_users as collection 

# Dark-themed Pokémon image
POKEMON_IMAGE_URL = "https://c4.wallpaperflare.com/wallpaper/578/604/890/hands-pokemon-ball-dark-wallpaper-preview.jpg"

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id=GROUP_ID, 
                                       text=f"✨ <b>New Trainer Joined!</b> ✨\n👤 User: <a href='tg://user?id={user_id}'>{escape(first_name)}</a>", 
                                       parse_mode='HTML')
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})
    
    if update.effective_chat.type == "private":
        caption = (
        "🔥 <b>Welcome, Trainer!</b> 🔥\n\n"
        "🎮 <b>I'm your Pokémon Card Collector Bot!</b> \n"
        "⚡ Add me to your group, and I'll drop Pokémon cards after a set number of messages.\n"
        "🛡️ Use <code>/guess</code> to collect them and build your ultimate collection!\n"
        "📜 View your Pokémon with <code>/collection</code>\n\n"
        "✨ <b>Catch 'Em All!</b> ✨"
        )
        
        keyboard = [
            [InlineKeyboardButton("⚡ ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("💬 SUPPORT", url=SUPPORT_CHAT),
            InlineKeyboardButton("📢 UPDATES", url=UPDATE_CHAT)],
            [InlineKeyboardButton("❓ HELP", callback_data='help')],
          ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=POKEMON_IMAGE_URL, caption=caption, reply_markup=reply_markup, parse_mode='HTML')
    else:
        keyboard = [
            [InlineKeyboardButton("⚡ ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("💬 SUPPORT", url=SUPPORT_CHAT),
            InlineKeyboardButton("📢 UPDATES", url=UPDATE_CHAT)],
            [InlineKeyboardButton("❓ HELP", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=POKEMON_IMAGE_URL, caption="🎴 **I'm active!** \nConnect with me in PM for more details!", reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = (
        "📜 **Trainer's Guide:**\n\n"
        "🔹 <code>/guess</code> - Capture Pokémon in groups!\n"
        "🔹 <code>/fav</code> - Set your favorite Pokémon!\n"
        "🔹 <code>/trade</code> - Trade Pokémon with others!\n"
        "🔹 <code>/gift</code> - Gift a Pokémon to a friend!\n"
        "🔹 <code>/collection</code> - View your Pokémon collection!\n"
        "🔹 <code>/topgroups</code> - See the most active Pokémon catching groups!\n"
        "🔹 <code>/top</code> - See the top trainers!\n"
        "🔹 <code>/ctop</code> - View your chat's top trainers!\n"
        "🔹 <code>/changetime</code> - Adjust Pokémon drop time (group admins only)\n"
        )
        help_keyboard = [[InlineKeyboardButton("⤾ Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='HTML')

    elif query.data == 'back':
        caption = (
        "🔥 <b>Welcome Back, Trainer!</b> 🔥\n\n"
        "🎮 <b>Catch Pokémon and build your collection!</b> \n"
        "⚡ Use <code>/guess</code> in groups to collect Pokémon!\n"
        "🛡️ View your Pokémon using <code>/collection</code>\n\n"
        "✨ <b>Gotta Catch 'Em All!</b> ✨"
        )
        keyboard = [
            [InlineKeyboardButton("⚡ ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("💬 SUPPORT", url=SUPPORT_CHAT),
            InlineKeyboardButton("📢 UPDATES", url=UPDATE_CHAT)],
            [InlineKeyboardButton("❓ HELP", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='HTML')

application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
