import qrcode
import tempfile

def generate_qr(data):
    qr = qrcode.QRCode(
        version=None,
        box_size=12,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp.name)
    return temp.name
