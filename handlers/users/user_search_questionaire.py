from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from loader import dp

from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from .utils import create_message_by_search_questionnaire


@dp.message_handler(text="Данные для поиска 🔍")
async def bot_start(message: types.Message):
    try:
        user = db.get_user(message.from_user.id)
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        q = db.get_questionnaire_by_user(user)
        message_text = create_message_by_search_questionnaire(q)
        await message.answer(message_text)
    except AttributeError:
        await message.answer("Чтобы воспользоваться ботом, Вам необходимо заполнить анкеты")

