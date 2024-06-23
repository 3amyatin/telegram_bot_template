from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, CommandStart, Command
from sqlalchemy import false

admin = Router()


class Admin(Filter):
    def __init__(self):
        self.admins = [197886110, 456]

    async def __call__(self, message: Message):
        if message.from_user is not None:
            return message.from_user.id in self.admins
        else:
            return false

@admin.message(Admin(), Command('admin'))
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бот, администратор!')