from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext

# from DB import *

# from helpers import wrap_tags, set_user_data
from inlinekeyboard import InlineKeyboard
from inlinekeyboard.inlinekeyboardvariables import *
from globals import *

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def callback_query_handler_callback(update: Update, context: CallbackContext):
    pass


callback_query_handler = CallbackQueryHandler(callback_query_handler_callback)
