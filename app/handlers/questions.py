from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from models import Question
from utils.state_manager import TestStates
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import SessionLocal

@dp.callback_query_handler(lambda c: c.data.startswith('test_'), state=TestStates.waiting_for_test_start)
async def load_questions(callback_query: types.CallbackQuery, state: FSMContext):
    test_id = int(callback_query.data.split('_')[1])
    
    async with SessionLocal() as session:
        # Fetch questions for the selected test
        questions = await session.execute(f"SELECT * FROM questions WHERE test_id = {test_id}")
        questions = questions.fetchall()
    
    if not questions:
        await callback_query.message.answer("No questions available for this test.")
        return
    
    # Shuffle questions if needed
    # questions = shuffle_questions(questions) # Implement shuffle logic if required
    
    await state.update_data(test_id=test_id, questions=questions, current_question=0)
    await send_question(callback_query.message, state)

async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    questions = data['questions']
    current_question = data['current_question']
    
    if current_question >= len(questions):
        await message.answer("Test completed!")
        await state.finish()
        return
    
    question = questions[current_question]
    keyboard = InlineKeyboardMarkup()
    for i in range(1, 5):
        keyboard.add(InlineKeyboardButton(question[f'answer{i}'], callback_data=f"answer_{i}"))
    
    await message.answer(question['question_text'], reply_markup=keyboard)
    await TestStates.waiting_for_answer.set()
    
@dp.callback_query_handler(lambda c: c.data.startswith('answer_'), state=TestStates.waiting_for_answer)
async def check_answer(callback_query: types.CallbackQuery, state: FSMContext):
    selected_answer = int(callback_query.data.split('_')[1])
    data = await state.get_data()
    questions = data['questions']
    current_question = data['current_question']
    question = questions[current_question]
    
    if selected_answer == question['correct_answer']:
        score = question['score_right']
        await callback_query.message.answer("Correct!")
    else:
        score = question['score_wrong']
        await callback_query.message.answer("Incorrect.")
    
    await state.update_data(current_question=current_question + 1)
    await send_question(callback_query.message, state)

    