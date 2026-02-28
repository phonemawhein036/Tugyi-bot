from telegram.ext import CallbackQueryHandler
from services.wireguard_service import generate_wireguard_config
from services.qr_service import generate_qr


def wireguard_key(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id

    conf_data = generate_wireguard_config(user_id)

    file_name = f"WG_{user_id}.conf"
    with open(file_name, "w") as f:
        f.write(conf_data)

    qr_path = generate_qr(conf_data, color="#ff6600", bg="white")

    context.bot.send_document(
        chat_id=query.message.chat_id,
        document=open(file_name, "rb"),
        filename=file_name
    )

    context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=open(qr_path, "rb"),
        caption="🔥 Phoenix Tugyi Warp QR"
    )


# 👇👇 ဒီထဲမှာထည့်ရမယ်
def register_buttons(dispatcher):
    dispatcher.add_handler(
        CallbackQueryHandler(wireguard_key, pattern="wireguard")
    )
