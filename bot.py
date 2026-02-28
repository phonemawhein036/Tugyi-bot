import os
import subprocess
import datetime
import qrcode
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

users = {}

async def getkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or str(user_id)
    today = datetime.date.today()

    if user_id in users and users[user_id] == today:
        await update.message.reply_text("❌ 1 Key per day limit.")
        return

    os.makedirs("temp", exist_ok=True)

    subprocess.run(["./wgcf", "register"], stdout=subprocess.DEVNULL)
    subprocess.run(["./wgcf", "generate"], stdout=subprocess.DEVNULL)

    conf_path = f"temp/{username}.conf"
    os.rename("wgcf-profile.conf", conf_path)

    with open(conf_path, "r") as f:
        config = f.read()

    qr = qrcode.make(config)
    qr_path = f"temp/{username}.png"
    qr.save(qr_path)

    await update.message.reply_document(InputFile(conf_path))
    await update.message.reply_photo(InputFile(qr_path))

    users[user_id] = today

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("getkey", getkey))

app.run_polling()
