from dotenv import load_dotenv
from telebot import types
from tgbot import bot

from doctors import logic

import os



def main():
    load_dotenv()
    token = os.getenv('token')
   
    if token:
       b = bot.BotInit(token=token)
       b.polling(none_stop=True, interval=0)
    else:
        print("TOKEN NOT FOUND")

        
if __name__ == "__main__":
    main()
