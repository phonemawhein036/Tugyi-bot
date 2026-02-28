import os
from telegram.ext import CallbackQueryHandler
from services.warp_service import generate_warp_config
from services.qr_service import generate_qr

def button_handler(update, context):
    query = update.callback_query
    query.answer()

    try:
        if query.data == "generate":
            query.edit_message_text("⏳ Generating your secure config...")

            # Generate config
            conf_path, conf_data = generate_warp_config(query.from_user.id)

            # Send .conf file
            query.message.reply_document(
                document=open(conf_path, "rb"),
                filename="PhoenixTugyiWarp.conf"
            )

            # Generate QR
            qr_path = generate_qr(conf_data, color="#ff6600", bg="white")

            query.message.reply_photo(
                photo=open(qr_path, "rb"),
                caption="*🔥 Phoenix Tugyi Warp Config*\n\n"
                        "✅ Scan QR to connect securely.",
                parse_mode="Markdown"
            )

            # Cleanup
            os.remove(conf_path)
            os.remove(qr_path)

            query.edit_message_text("✅ Config generated successfully 🚀")

        elif query.data == "region":
            query.edit_message_text("🌍 Region system coming in Phase 3.")

        elif query.data == "account":
            query.edit_message_text("👤 Account system coming soon.")

    except Exception as e:
        query.message.reply_text("❌ System error occurred. Please try again.")

def register_buttons(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
