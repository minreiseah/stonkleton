""" Starts the bot
"""

import os
import logging
from dotenv import load_dotenv

from telebot.bot import Bot

def main():
    # Basic Setup
    load_dotenv()
    logging.basicConfig(filename='telebotlog.log', filemode='w', level=logging.INFO,   
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Get token from env 
    try:
        token = os.environ.get('TELEGRAM_API_TOKEN')
    except KeyError as err:
        logging.error(err)

    try:    
        bot = Bot(token)
        bot.run()
    except Exception as err:
        logging.error('Bot failed to start.')
        logging.error(err)


if __name__ == '__main__':
    main()