from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters, \
    CallbackQueryHandler

from config import ACTIVE_ADMINS
from DB import insert_data
from helpers import create_certificate
from globals import *

from inlinekeyboard import InlineKeyboard
from inlinekeyboard.inlinekeyboardvariables import *

import logging
import datetime
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def do_command(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data
    user_id = update.effective_user.id

    if user_id not in ACTIVE_ADMINS:
        text = '😔 Kechirasiz men faqat adminlar uchun xizmat qilaman !\n\n' \
               'Adminga murojaat qilish uchun @Baxa0715 ga yozing !'
        update.message.reply_text(text)

        state = ConversationHandler.END

    else:
        text = "O'rinni tanlang:"
        inline_keyboard = InlineKeyboard(choose_place_keyboard, 'uz').get_keyboard()

        message = update.message.reply_text(text, reply_markup=inline_keyboard)

        state = CHOOSE_PLACE
        user_data['message_id'] = message.message_id

    return state


def choose_place_callback(update: Update, context: CallbackContext):
    user_data = context.user_data

    callback_query = update.callback_query
    place = callback_query.data

    if 'certs' in user_data and place in user_data['certs']:
        callback_query.answer(f"{place} - o'rin uchun sertifikat tasdiqlangan !\n"
                              f"Boshqa o'rinni tanlang !", show_alert=True)

        state = None

    else:
        callback_query.answer()
        text = f"{place} - o'rin uchun to'liq ism, familya va sharifni yuboring"
        callback_query.edit_message_text(text)

        state = FULLNAME
        user_data['place'] = place

    return state


def fullname_callback(update: Update, context: CallbackContext):
    user_data = context.user_data

    gold_medal = '🥇'
    silver_medal = '🥈'
    bronze_medal = '🥉'

    fullname = update.message.text
    place = user_data['place']
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    medal = gold_medal if place == '1' else silver_medal if place == '2' else bronze_medal

    certificate = create_certificate(place, fullname, date)
    caption = f"{medal} {place} - o'rin: {fullname}"

    inline_keyboard = InlineKeyboard(confirm_keyboard, 'uz').get_keyboard()
    message = update.message.reply_photo(certificate['cert_url'], caption, reply_markup=inline_keyboard)

    if 'certs' not in user_data:
        user_data['certs'] = {place: certificate}
    else:
        user_data['certs'].update({place: certificate})

    state = CONFIRMATION
    user_data['fullname'] = fullname
    user_data['message_id'] = message.message_id

    # logger.info('user_data: %s', user_data)
    return state


def confirmation_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    callback_query = update.callback_query

    if callback_query.data == 'cancel':
        # Remove certificate from the location
        os.remove(user_data['certs'][user_data['place']]['cert_path'])

        # Remove QR code from the location
        os.remove(user_data['certs'][user_data['place']]['qr_code_path'])

        # delete user_data dict
        del user_data['certs'][user_data['place']]

        callback_query.message.delete()

        text = "O'rinni tanlang:"
        inline_keyboard = InlineKeyboard(choose_place_keyboard, 'uz').get_keyboard()

        message = callback_query.message.reply_text(text, reply_markup=inline_keyboard)

        state = CHOOSE_PLACE
        user_data['message_id'] = message.message_id

    else:
        callback_query.edit_message_reply_markup()

        data = {
            'cert_url': user_data['certs'][user_data['place']]['cert_url'],
            'cert_qr_code': user_data['certs'][user_data['place']]['qr_code_path'].split('/')[-1],
            'fullname': user_data['fullname'],
            'place': user_data['place']
        }
        insert_data(data, table_name='certificates')

        if len(user_data['certs']) == 3:
            callback_query.answer("Barcha o'rinlar uchun sertifikatlar tasqdiqlandi !")

            callback_query.message.reply_media_group([
                InputMediaPhoto(user_data['certs']['1']['cert_url']),
                InputMediaPhoto(user_data['certs']['2']['cert_url']),
                InputMediaPhoto(user_data['certs']['3']['cert_url'])
            ])

            user_data.clear()

            state = ConversationHandler.END

        else:

            text = "O'rinni tanlang:"
            inline_keyboard = InlineKeyboard(choose_place_keyboard, 'uz').get_keyboard()

            message = callback_query.message.reply_text(text, reply_markup=inline_keyboard)

            state = CHOOSE_PLACE
            user_data['message_id'] = message.message_id

    # logger.info('user_data: %s', user_data)
    return state


def cancel_callback(update: Update, context: CallbackContext):
    user_data = context.user_data

    context.bot.delete_message(ACTIVE_ADMINS[0], user_data['message_id'])

    update.message.reply_text('Sertifikat berish bekor qilindi !\n\n'
                              'Sertifikat berishni boshlash uchun /certificate komandasini yuboring !')

    user_data.clear()
    return ConversationHandler.END


certificate_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['certificate'], do_command, filters=~Filters.update.edited_message),
    ],

    states={

        CHOOSE_PLACE: [CallbackQueryHandler(choose_place_callback, pattern=r'^(\d)$')],

        FULLNAME: [MessageHandler(Filters.text & (~ Filters.command), fullname_callback)],

        CONFIRMATION: [CallbackQueryHandler(confirmation_callback, pattern=r'^(confirm|cancel)$')]
    },

    fallbacks=[
        CommandHandler(['cancel'], cancel_callback, filters=~Filters.update.edited_message),
    ],

    persistent=True,

    name='certificate_conversation'
)
