from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData('yes_or_no', 'question', 'choice')


def yes_or_no_markup(question, does_not_matter=False):
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
            callback_data=yes_or_no_callback.new(question, 'no'),
        )
    )
    if does_not_matter:
        markup.add(
            InlineKeyboardButton(
                text="Не имеет значения",
                callback_data=yes_or_no_callback.new(question, 'does_not_matter')
            )
        )
    return markup


