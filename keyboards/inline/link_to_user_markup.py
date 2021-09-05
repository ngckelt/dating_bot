from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData('yes_or_no', 'question', 'choice')
user_data_callback = CallbackData('show_user_data', 'user_data_id')


def link_to_user_markup(username):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Перейти к пользователю",
            url=f"https://t.me/{username}"
        )
    )
    return markup


def show_user_data_markup(user_data_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Данные пользователя",
            callback_data=user_data_callback.new(user_data_id)
        )
    )
    return markup



