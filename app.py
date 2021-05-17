from io import StringIO, BytesIO

import qrcode
from flask import Flask, send_file, request

app = Flask(__name__)

ECL_DICT = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
        }


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/qr")
def gen_qr_code():
    """
    http://127.0.0.1:8000/qr?data=http://www.google.com&ecl=H&v=1&border=1&size=200
    """
    data = request.args.get("data")
    size = request.args.get("size", 250)
    # error_correction_level
    ecl = request.args.get("ecl", "H")
    # version 1, is a 21x21 matrix
    version = request.args.get("v", 1)
    border = request.args.get("border", 0)

    box_size = int(size)/27
    qr = qrcode.QRCode(
        version=version,
        error_correction=ECL_DICT.get(ecl.upper(), qrcode.constants.ERROR_CORRECT_H),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()

    output = BytesIO()
    img.save(output, "PNG")
    output.seek(0)

    return send_file(output, mimetype='image/png')