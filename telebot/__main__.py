""" Starts the bot
"""

import os
import logging
from dotenv import load_dotenv

from telebot.bot import Bot

def main():
    # Basic Setup
    load_dotenv()
    logging.basicConfig(filename='telebotlog.log', filemode='w', level=logging.DEBUG,   
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # get token from env 
    try:
        token = os.environ.get('TELEGRAM_API_TOKEN')
        
    except KeyError as err:
        logging.error(err)
    
    bot = Bot(token)
    pass


if __name__ == '__main__':
    main()