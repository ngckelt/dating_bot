from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_markup():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Мои данные ✅"),
                KeyboardButton(text=f"Данные для поиска 🔍"),
            ],
            [
                KeyboardButton(text=f"Изменить данные о себе ✏️"),
                KeyboardButton(text=f"Изменить данные для поиска 📝"),
            ],
            [
                KeyboardButton(text=f"Удалить мои данные ❌️"),
                KeyboardButton(text=f"Изменить статус для поиска️"),
            ],
        ],
        resize_keyboard=True
    )

    return markup

