import os, subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def generate(update, context):
    await update.message.reply_text("⏳ Phoenix Mobile Tugyi v3.1 ကနေ Config ထုတ်ပေးနေပါပြီ...")
    try:
        # Permission ပေးခြင်း
        os.chmod("./wgcf", 0o755)
        # Config ထုတ်ခြင်း
        subprocess.run(["./wgcf", "register", "--accept-tos"], check=True)
        subprocess.run(["./wgcf", "generate"], check=True)
        
        # Endpoint နှင့် DNS ပြင်ဆင်ခြင်း
        with open("wgcf-profile.conf", "r") as f:
            lines = f.readlines()
        with open("Phoenix.conf", "w") as f:
            for line in lines:
                if line.startswith("DNS"): f.write("DNS = 8.8.8.8\n")
                elif line.startswith("Endpoint"): f.write("Endpoint = 162.159.192.10:500\n")
                else: f.write(line)

        with open("Phoenix.conf", "rb") as f:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=f, filename="Phoenix_V3.1.conf")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("generate", generate))
    app.run_polling()
