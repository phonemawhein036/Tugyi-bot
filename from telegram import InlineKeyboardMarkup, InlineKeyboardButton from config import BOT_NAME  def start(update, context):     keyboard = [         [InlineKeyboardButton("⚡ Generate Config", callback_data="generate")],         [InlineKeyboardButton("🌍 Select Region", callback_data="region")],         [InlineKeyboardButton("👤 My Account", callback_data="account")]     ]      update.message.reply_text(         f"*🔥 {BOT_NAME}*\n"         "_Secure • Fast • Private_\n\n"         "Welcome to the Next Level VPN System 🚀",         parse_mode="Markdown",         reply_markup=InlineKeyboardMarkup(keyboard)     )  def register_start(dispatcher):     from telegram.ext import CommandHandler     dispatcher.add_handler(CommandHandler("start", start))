from telegram.ext import CallbackQueryHandler

def button_handler(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "generate":
        query.edit_message_text("⏳ Generating your config...")

    elif query.data == "region":
        query.edit_message_text("🌍 Region selector coming soon...")

    elif query.data == "account":
        query.edit_message_text("👤 Account system loading...")

def register_buttons(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
