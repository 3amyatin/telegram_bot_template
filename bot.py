# https://docs.aiogram.dev/en/dev-3.x/api/index.html

import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

#from handlers import start, test, questions
from app.handlers import router
from app.admin import admin
from app.user import user


#start.register_handlers_start(dp)
#test.register_handlers_test(dp)
#questions.register_handlers_questions(dp)

async def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    if TELEGRAM_TOKEN is None:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")
    
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit by Ctrl-C')
