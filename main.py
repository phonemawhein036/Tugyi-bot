import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, Dispatcher
from config import TOKEN, BOT_NAME
from handlers.start_handler import register_start
from handlers.button_handler import register_buttons
from database import init_db

app = Flask(__name__)
bot = Bot(token=TOKEN)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Initialize Database
init_db()

# Register Handlers
register_start(dispatcher)
register_buttons(dispatcher)

# Webhook Route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Home Route (Render needs open port)
@app.route("/")
def home():
    return f"{BOT_NAME} is Live 🚀"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))

    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if RENDER_EXTERNAL_URL:
        bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/{TOKEN}")

    app.run(host="0.0.0.0", port=PORT)
