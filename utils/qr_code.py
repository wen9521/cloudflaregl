import qrcode
from io import BytesIO

def generate_qr_code(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    bio = BytesIO()
    bio.name = "qrcode.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio