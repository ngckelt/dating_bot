from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

confirm_callback = CallbackData('confirm', 'question', 'choice')


def confirm_markup(question):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Подтверждаю",
            callback_data=confirm_callback.new(question, 'True')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=confirm_callback.new(question, 'False')
        )
    )
    return markup


