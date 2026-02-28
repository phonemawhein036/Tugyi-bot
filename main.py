import os
import subprocess
import qrcode
from flask import Flask, request
from telegram import Bot, Update, InputFile
from telegram.ext import Dispatcher, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /generate to create WGCF key")

# GENERATE COMMAND
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username or str(update.message.from_user.id)
    filename = f"{user}.conf"

    # Run wgcf
    subprocess.run(["wgcf", "register"])
    subprocess.run(["wgcf", "generate"])

    os.rename("wgcf-profile.conf", filename)

    # Send config file
    await update.message.reply_document(InputFile(filename))

    # Generate QR
    img = qrcode.make(open(filename).read())
    img.save("qr.png")
    await update.message.reply_photo(photo=open("qr.png", "rb"))

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("generate", generate))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot running"
