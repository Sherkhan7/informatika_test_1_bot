from PIL import Image, ImageFont, ImageDraw
from config import CERTIFICATES_URL

import requests
import datetime


# from DB import get_user


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


def wrap_tags(*args):
    symbol = ' ' if len(args) > 1 else ''

    return f'<b><i><u>{symbol.join(args)}</u></i></b>'


def create_certificate(place, fullname, date):
    template_name = f'{place}_place'
    template_ext = '.png'
    template_full_name = './cert_templates/' + template_name + template_ext
    font_path = './fonts/PlayfairDisplay/static/PlayfairDisplay-ExtraBoldItalic.ttf'
    font_size = 30
    font_color = (16, 2, 58, 255)  # Dark blue

    certificate_name = 'cert_' + date
    certificate_ext = '.png'
    certificate_full_name = CERTIFICATES_URL + certificate_name + certificate_ext

    cert_template = Image.open(template_full_name)
    font = ImageFont.truetype(font_path, size=font_size)
    image_editable = ImageDraw.Draw(cert_template)

    width, height = font.getsize(fullname)
    image_editable.text(((cert_template.width - width) / 2, (cert_template.height - height) / 3.23),
                        fullname, font_color, font=font)

    # params = {
    #     'data': 'https://cardel.ml',
    #     'size': '100x100',), title_text, (237, 230, 0), font_path=title_font)
    # cert_template.save("result.png")
    #     'margin': 1,
    # }
    # #
    # server_response = requests.post('http://api.qrserver.com/v1/create-qr-code/', data=params)
    #
    # file = open("photo.png", "wb")
    # file.write(server_response.content)
    # file.close()

    # qr_code = Image.open('photo.png')
    # img_copy = cert_template.copy()
    # position = ((img_copy.width - qr_code.width), (img_copy.height - qr_code.height))
    # img_copy.paste(qr_code, (0, (img_copy.height - qr_code.height)), 1)
    # img_copy.save('test.jpeg')

    # Save new certificate
    cert_template.save(certificate_full_name)

    return certificate_full_name


# fullname = 'dsdsd'
# place = '1'
# date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# print(create_certificate(place, fullname, date))
