import os
from telegram.ext import CallbackQueryHandler
from services.wireguard_service import generate_wireguard_config
from services.qr_service import generate_qr
from database import can_generate


def wireguard_key(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    chat_id = query.message.chat_id

    # 🔐 Daily 1 Key Limit Check
    if not can_generate(user_id):
        context.bot.send_message(
            chat_id=chat_id,
            text="🚫 You can only generate 1 key per day.\n\nTry again tomorrow 🔥"
        )
        return

    try:
        # Generate WireGuard config
        conf_data = generate_wireguard_config(user_id)

        file_name = f"Phoenix_{user_id}.conf"
        with open(file_name, "w") as f:
            f.write(conf_data)

        # 🎨 Phoenix Orange QR
        qr_path = generate_qr(conf_data, color="#ff6600", bg="white")

        # Send .conf file
        context.bot.send_document(
            chat_id=chat_id,
            document=open(file_name, "rb"),
            filename=file_name,
            caption="🔥 Phoenix Tugyi Warp Config"
        )

        # Send QR Code
        context.bot.send_photo(
            chat_id=chat_id,
            photo=open(qr_path, "rb"),
            caption="📱 Scan QR to Connect\n\nPhoenix Tugyi Warp 🚀"
        )

        # 🧹 Auto Cleanup
        os.remove(file_name)
        os.remove(qr_path)

    except Exception as e:
        context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ Error occurred:\n{str(e)}"
        )


def register_buttons(dispatcher):
    dispatcher.add_handler(
        CallbackQueryHandler(wireguard_key, pattern="wireguard")
    )
