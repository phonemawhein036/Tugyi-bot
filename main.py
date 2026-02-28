import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, Dispatcher

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
bot = Bot(token=TOKEN)

# Telegram Updater (v13 style)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher


# ✅ Start command
def start(update, context):
    update.message.reply_text("Bot is running successfully 🚀")


dispatcher.add_handler(CommandHandler("start", start))


# ✅ Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"


# ✅ Home route (Render needs open port)
@app.route("/")
def home():
    return "Bot is alive!"


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))

    # Set webhook (Render URL automatically)
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if RENDER_EXTERNAL_URL:
        bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/{TOKEN}")

    app.run(host="0.0.0.0", port=PORT)
