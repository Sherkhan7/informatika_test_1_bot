from telegram.ext import Updater, PicklePersistence
from config import TOKEN, BASE_URL, PORT
from errorhandler import error_handler
from handlers import certificate_conversation_handler, command_handler


def main():
    my_persistence = PicklePersistence(filename='my_pickle', single_file=False, store_chat_data=False)

    updater = Updater(TOKEN, persistence=my_persistence)

    updater.dispatcher.add_handler(certificate_conversation_handler)

    updater.dispatcher.add_handler(command_handler)

    updater.dispatcher.add_error_handler(error_handler)

    # updater.start_polling()
    # updater.idle()
    
    updater.start_webhook(port=PORT, url_path=TOKEN, webhook_url=BASE_URL + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
