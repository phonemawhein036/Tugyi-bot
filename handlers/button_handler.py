import os
import time
from telegram.ext import CallbackQueryHandler
from services.wireguard_service import generate_wireguard_config
from services.qr_service import generate_qr
from database import can_generate

# ⚡ Anti-Spam Storage (in memory)
user_last_click = {}

# ⏳ Cooldown seconds
COOLDOWN = 5   # 5 seconds


def wireguard_key(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    chat_id = query.message.chat_id
    current_time = time.time()

    # ⚡ Anti-Spam Check
    if user_id in user_last_click:
        if current_time - user_last_click[user_id] < COOLDOWN:
            context.bot.send_message(
                chat_id=chat_id,
                text="⚡ Slow down!\nPlease wait a few seconds before trying again."
            )
            return

    user_last_click[user_id] = current_time

    # 🔐 Daily 1 Key Limit Check
    if not can_generate(user_id):
        context.bot.send_message(
            chat_id=chat_id,
            text="🚫 You can only generate 1 key per day.\n\nTry again tomorrow 🔥"
        )
        return

    try:
        # Generate config
        conf_data = generate_wireguard_config(user_id)

        file_name = f"Phoenix_{user_id}.conf"
        with open(file_name, "w") as f:
            f.write(conf_data)

        # 🎨 Phoenix Orange QR
        qr_path = generate_qr(conf_data, color="#ff6600", bg="white")

        # Send .conf
        context.bot.send_document(
            chat_id=chat_id,
            document=open(file_name, "rb"),
            filename=file_name,
            caption="🔥 Phoenix Tugyi Warp Config"
        )

        # Send QR
        context.bot.send_photo(
            chat_id=chat_id,
            photo=open(qr_path, "rb"),
            caption="📱 Scan QR to Connect\n\nPhoenix Tugyi Warp 🚀"
        )

        # 🧹 Cleanup
        os.remove(file_name)
        os.remove(qr_path)

    except Exception as e:
        context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ Error:\n{str(e)}"
        )


def register_buttons(dispatcher):
    dispatcher.add_handler(
        CallbackQueryHandler(wireguard_key, pattern="wireguard")
    )
