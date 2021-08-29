from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData('yes_or_no', 'question', 'choice')


def link_to_user_markup(username):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Перейти к пользователю",
            url=f"https://t.me/{username}"
        )
    )
    return markup


