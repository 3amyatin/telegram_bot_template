# Backend: /Users/digy/dev/yachtsam_bot/
# Frontend: https://t.me/sailgpt_bot

import os
import asyncio  # https://docs.aiogram.dev/en/dev-3.x/api/index.html
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

#from handlers import start, test, questions
from app.user import user
from app.admin import admin
from app.handlers import router
from app.db.models import async_main


#start.register_handlers_start(dp)
#test.register_handlers_test(dp)
#questions.register_handlers_questions(dp)

async def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    if TELEGRAM_TOKEN is None:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")
    
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.include_router(router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
    await async_main()  # Create tables if not exists
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit by Ctrl-C')
