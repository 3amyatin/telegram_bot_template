from calendar import c
from operator import call
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Тесты', callback_data='tests')], 
        [KeyboardButton(text='Результаты', callback_data='results')],
        [KeyboardButton(text='Помощь', callback_data='help')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)

ABCD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='A', callback_data='button_A')],
        [InlineKeyboardButton(text='B', callback_data='button_B')],
        [InlineKeyboardButton(text='C', callback_data='button_C')],
        [InlineKeyboardButton(text='D', callback_data='button_D')],
    ],
    input_field_placeholder='Выберите вариант ответа'
)


# async def catalog():
#     keyboard = InlineKeyboardBuilder()
#     for item in sneaker_brands:
#         keyboard.add(InlineKeyboardButton(text=item, callback_data=f'sneakers_{item}'))
#     return keyboard.adjust(2).as_markup()
