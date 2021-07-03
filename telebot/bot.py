import logging

# Add PicklePersistence later
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from stock import Stock

class Bot:
    """Bot class that does things

    Attributes:
        token: Telegram API token.

    Methods:
        run: Invokes Updater to start polling.
    """

    def __init__(self, token) -> None:
        self.token = token

    

