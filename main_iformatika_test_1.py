from telegram.ext import Updater, PicklePersistence
from telegram import Update

from config import TOKEN
import logging

from handlers import message_handler, callback_query_handler, sertificate_conversation_handler, command_handler


def main():
    my_persistence = PicklePersistence(filename='my_pickle', single_file=False, store_chat_data=False)

    updater = Updater(TOKEN, persistence=my_persistence)

    updater.dispatcher.add_handler(sertificate_conversation_handler)
    #
    # updater.dispatcher.add_handler(message_handler)
    #
    updater.dispatcher.add_handler(callback_query_handler)

    updater.dispatcher.add_handler(command_handler)

    updater.start_polling()
    updater.idle()

    # updater.start_webhook(listen='127.0.0.1', port=5008, url_path=TOKEN)
    # updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    # updater.idle()


if __name__ == '__main__':
    main()
