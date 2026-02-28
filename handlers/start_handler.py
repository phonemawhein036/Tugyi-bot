from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_NAME

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("⚡ Generate Config", callback_data="generate")],
        [InlineKeyboardButton("🌍 Select Region", callback_data="region")],
        [InlineKeyboardButton("👤 My Account", callback_data="account")]
    ]

    update.message.reply_text(
        f"*🔥 {BOT_NAME}*\n"
        "_Secure • Fast • Private_\n\n"
        "Welcome to the Next Level VPN System 🚀",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def register_start(dispatcher):
    from telegram.ext import CommandHandler
    dispatcher.add_handler(CommandHandler("start", start))
