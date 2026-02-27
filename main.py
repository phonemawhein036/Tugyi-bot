import os, subprocess, urllib.request, qrcode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# WGCF Binary ကို Auto Download ဆွဲခြင်း
def download_wgcf():
    if not os.path.exists("wgcf"):
        url = "https://github.com/ViRb3/wgcf/releases/download/v2.2.22/wgcf_2.2.22_linux_amd64"
        urllib.request.urlretrieve(url, "wgcf")
        os.chmod("./wgcf", 0o755)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Wireguard Key", callback_data='gen_wg')],
        [InlineKeyboardButton("💎 VIP Info", callback_data='vip'), InlineKeyboardButton("📢 Join Channel", url='https://t.me/your_channel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("လိုင်းကောင်းတဲ့ VPN Key ထုတ်နိုင်ပါပြီ\nအောက်မှ ခလုတ်များကိုနှိပ်ပြီး ထုတ်ယူပါ", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'gen_wg':
        await query.edit_message_text("⏳ Phoenix Mobile Tugyi v3.1 ကနေ ထုတ်ပေးနေပါပြီ...")
        download_wgcf()
        
        try:
            # Config ထုတ်ခြင်း Logic
            subprocess.run(["./wgcf", "register", "--accept-tos"], check=True)
            subprocess.run(["./wgcf", "generate"], check=True)
            
            # Endpoint 162.159.192.10:500 နှင့် DNS 8.8.8.8 သတ်မှတ်ခြင်း
            with open("wgcf-profile.conf", "r") as f:
                content = f.read().replace("162.159.193.10:2408", "162.159.192.10:500").replace("1.1.1.1", "8.8.8.8")
            
            with open("Phoenix.conf", "w") as f: f.write(content)

            # QR Code ထုတ်ခြင်း
            qr = qrcode.make(content)
            qr.save("Phoenix_QR.png")

            # ဖိုင်နှင့် QR ပို့ခြင်း
            await query.message.reply_document(document=open("Phoenix.conf", "rb"), filename="Phoenix_V3.1.conf")
            await query.message.reply_photo(photo=open("Phoenix_QR.png", "rb"), caption="📱 QR Code Scan ဖတ်ပြီး သုံးနိုင်ပါပြီ")
            
        except Exception as e:
            await query.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
