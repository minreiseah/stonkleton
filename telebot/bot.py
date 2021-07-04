import logging

# Add PicklePersistence later
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from stock import Stock

class Bot:
    """Base class for a telegram bot.

    Attributes:
        token: Telegram API token.
        updater: Updater object.
        dispatcher: Dispatcher object.

    Methods:
        run: Invokes Updater to start polling.
        start: Basic command to start the bot. Meant to be by subclass.
        echo: Test to check if Bot is functional.
    """

    def __init__(self, token) -> None:
        self.token = token
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        # Handlers
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text & (~Filters.command), self.echo)
        self.dispatcher.add_handler(echo_handler)
    
    def run(self) -> None:
        self.updater.start_polling()
        self.updater.idle()
        logging.info('Base Bot started successfully!')
    
    def start(self, update:Update, context:CallbackContext) -> None:
        chat_id = update.effective_chat.id
        text = "Hello! You've activated the Base Bot!" 
        context.bot.send_message(chat_id=chat_id, text=text)
    
    def echo(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        text = update.message.text
        context.bot.send_message(chat_id=chat_id, text=text)

