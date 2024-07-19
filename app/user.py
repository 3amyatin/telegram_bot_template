from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.db.requests import set_user

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user is not None:
        await set_user(tg_id=message.from_user.id, name=message.from_user.full_name)
    await message.answer('Добро пожаловать в бот!')