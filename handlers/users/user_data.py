from pprint import pprint
import json

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from loader import dp

from utils.db_api import botdb as db
from .utils import create_message_by_user_questionnaire
from utils.cupid import cupid


@dp.message_handler(text="Мои данные ✅")
async def user_data(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user is not None:
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        message_text = create_message_by_user_questionnaire(user)
        await message.answer(message_text, parse_mode="HTML")
    else:
        await message.answer("Чтобы воспользоваться ботом, Вам необходимо заполнить анкеты")



