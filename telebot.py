from telegram.ext import (
    Updater, 
    CommandHandler, 
    ConversationHandler, 
    MessageHandler,
    Filters,
    CallbackContext
)
from telegram import Update
from config import TOKEN

import handlers
import logging

GENDER, AGE, WEIGHT, HEIGHT = range(4)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token = TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', handlers.start)
    dispatcher.add_handler(start_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('bmr', handlers.bmr)],
        states={
            GENDER: [MessageHandler(Filters.text, handlers.gender)],
            AGE: [MessageHandler(Filters.text, handlers.age)],
            WEIGHT: [MessageHandler(Filters.text, handlers.weight)],
            HEIGHT: [MessageHandler(Filters.text, handlers.height)]
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
