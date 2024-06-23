from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp

@dp.message_handler(Command("start"), state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Welcome to the Educational Test Bot! Use /test to start a test.")