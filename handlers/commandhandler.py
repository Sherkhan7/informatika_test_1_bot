from telegram import Update
from telegram.ext import Filters, CommandHandler, CallbackContext

from config import GROUP_USERNAME


def start_command_callback(update: Update, context: CallbackContext):
    text = f'Assalomua alaykum {update.effective_user.first_name} !\n\n' \
           f'{GROUP_USERNAME} guruhining rasmiy Telegram botiga xush kelibsiz !\n\n' \
           f'Sertifikat berishni boshlash uchun /certificate komandasini yuboring !'

    update.message.reply_text(text)


command_handler = CommandHandler('start', start_command_callback, filters=~Filters.update.edited_message)
