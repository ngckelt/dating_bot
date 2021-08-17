from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData('yes_or_no', 'question', 'choice')


def yes_or_no_markup(question):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Да",
            callback_data=yes_or_no_callback.new(question, 'yes')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Нет",
            callback_data=yes_or_no_callback.new(question, 'no')
        )
    )
    return markup


