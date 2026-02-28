from services.wireguard_service import generate_wireguard_config
from services.qr_service import generate_qr

def wireguard_key(update, context):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id

    # 1️⃣ Generate config text
    conf_data = generate_wireguard_config(user_id)

    # 2️⃣ Save .conf file
    file_name = f"WG_{user_id}.conf"
    with open(file_name, "w") as f:
        f.write(conf_data)

    # 3️⃣ Generate QR (Phoenix Orange 🔥)
    qr_path = generate_qr(conf_data, color="#ff6600", bg="white")

    # 4️⃣ Send conf file
    context.bot.send_document(
        chat_id=query.message.chat_id,
        document=open(file_name, "rb"),
        filename=file_name,
        caption="⚡ Wireguard Config File"
    )

    # 5️⃣ Send QR
    context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=open(qr_path, "rb"),
        caption="🔥 Phoenix Tugyi Warp QR\n\nScan to connect securely.",
        parse_mode="Markdown"
    )
