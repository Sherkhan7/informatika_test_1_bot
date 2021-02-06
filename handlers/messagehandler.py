from telegram import Update
from telegram.ext import Filters, MessageHandler, CallbackContext

# from helpers import set_user_data
from replykeyboard.replykeyboardtypes import reply_keyboard_types
from replykeyboard.replykeyboardvariables import *

from inlinekeyboard import InlineKeyboard
from inlinekeyboard.inlinekeyboardvariables import *
from globals import *


def message_handler_callback(update: Update, context: CallbackContext):
    pass


message_handler = MessageHandler(Filters.text & (~ Filters.command), message_handler_callback)
