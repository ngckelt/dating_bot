from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from loader import dp

from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from .utils import create_message_by_user_questionnaire


@dp.message_handler(text="Мои данные")
async def bot_start(message: types.Message):
    user = db.get_user(message.from_user.id)
    message_text = create_message_by_user_questionnaire(user)
    await message.answer(message_text)



