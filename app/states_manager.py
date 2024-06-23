from aiogram.dispatcher.filters.state import State, StatesGroup

class TestStates(StatesGroup):
    waiting_for_test_start = State()
    waiting_for_answer = State()