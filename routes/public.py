import qrcode
from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

# =========================
# TELA PRINCIPAL DE CHECK-IN
# =========================
@public_bp.route('/')
def checkin():
    return render_template('checkin.html')


# =========================
# GERAR QR CODE DO CHECK-IN
# =========================
@public_bp.route('/qr')
def qr_code():
    url_checkin = 'http://127.0.0.1:5000/'

    img = qrcode.make(url_checkin)
    img.save('static/qrcode.png')

    return render_template('qr.html')
