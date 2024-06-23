from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from models import Test
from utils.state_manager import TestStates
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import SessionLocal

@dp.message_handler(Command("test"), state="*")
async def start_test(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        # Fetch available tests from the database
        tests = await session.execute("SELECT * FROM tests")
        tests = tests.fetchall()
    
    if not tests:
        await message.answer("No tests available.")
        return
    
    keyboard = InlineKeyboardMarkup()
    for test in tests:
        keyboard.add(InlineKeyboardButton(test.name, callback_data=f"test_{test.id}"))
    
    await message.answer("Select a test:", reply_markup=keyboard)
    await TestStates.waiting_for_test_start.set()