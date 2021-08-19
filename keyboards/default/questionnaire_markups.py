from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize


def cancel_fill_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Заполнить анкету заново 🔄"),
            ],
            [
                KeyboardButton(text=f"Отменить заполнение анкеты ❌"),
            ],
        ],
        resize_keyboard=True
    )

    return markup


def fill_user_questionnaire():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Заполнить анкету о себе 📝"),
            ],
        ],
        resize_keyboard=True
    )

    return markup


def fill_search_questionnaire():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Заполнить анкету для поиска 📝"),
            ],
        ],
        resize_keyboard=True
    )

    return markup

