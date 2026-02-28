import qrcode
import tempfile

def generate_qr(data, color="black", bg="white"):
    qr = qrcode.QRCode(
        version=None,
        box_size=12,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color=bg)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp.name)
    return temp.name
