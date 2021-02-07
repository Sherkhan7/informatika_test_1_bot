from PIL import Image, ImageFont, ImageDraw
from config import CERTIFICATES_URL, QR_CODES_PATH, CERTIFICATES_PATH

import requests
import datetime


# def set_user_data(user_id, user_data):
#     value = user_data.setdefault('user_data', None)
#
#     if not value:
#         value = get_user(user_id)
#
#         if value:
#             value.pop('created_at')
#             value.pop('updated_at')
#
#         user_data['user_data'] = value


# def wrap_tags(*args):
#     symbol = ' ' if len(args) > 1 else ''
#
#     return f'<b><i><u>{symbol.join(args)}</u></i></b>'


def create_certificate(place, fullname, date):
    # Template
    template_name = f'{place}_place'
    template_ext = '.png'
    template_path = './cert_templates/' + template_name + template_ext

    # Font
    font_path = './fonts/PlayfairDisplay/static/PlayfairDisplay-ExtraBoldItalic.ttf'
    font_size = 24
    font_color = (16, 2, 58, 255)  # Dark blue

    # Certificate
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    certificate_name = 'cert_' + current_datetime
    certificate_ext = '.png'
    certificate_path = CERTIFICATES_PATH + certificate_name + certificate_ext

    cert_template = Image.open(template_path)
    font = ImageFont.truetype(font_path, size=font_size)
    image_editable = ImageDraw.Draw(cert_template)

    # Fullname text size
    width, height = font.getsize(fullname)

    # Date text size
    width_2, height_2 = font.getsize(date)

    # Write fullname to the certificate
    image_editable.text(((cert_template.width - width) / 2, (cert_template.height - height) / 3.23),
                        fullname, font_color, font=font)

    # Write date to the certificate
    image_editable.text(((cert_template.width - width_2) / 3, (cert_template.height - height_2) / 1.25),
                        date, font_color, font=font)

    # Qr code parameters
    qr_code_params = {
        'data': CERTIFICATES_URL + certificate_name + certificate_ext,
        'size': '90x90',
        'margin': 2,
    }
    server_response = requests.post('http://api.qrserver.com/v1/create-qr-code/', data=qr_code_params)

    qr_code_path = f'{QR_CODES_PATH}qr_{current_datetime}.png'

    # Save QR code to the folder
    file = open(qr_code_path, "wb")
    file.write(server_response.content)
    file.close()

    # QR code paste
    qr_code = Image.open(qr_code_path)
    # position = ((cert_template.width - qr_code.width), (cert_template.height - qr_code.height))
    cert_template.paste(qr_code, (0, (cert_template.height - qr_code.height)))

    # Save new certificate
    cert_template.save(certificate_path)

    return {
        'cert_url': CERTIFICATES_URL + certificate_name + certificate_ext,
        'cert_path': certificate_path,
        'qr_code_path': qr_code_path
    }
