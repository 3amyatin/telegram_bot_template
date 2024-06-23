from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в бот для обучения и прохождения тестов!")
    #await state.clear()

@router.message(Command('debug'))
async def debug(message: Message):
    await message.answer(str(message))

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await message.reply(str(message.text) + ": Тесты пока не готовы, но скоро будут!")
    #await state.clear()