from pprint import pprint
import json

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from loader import dp

from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from .utils import create_message_by_user_questionnaire
from utils.cupid import cupid


@dp.message_handler(text="Мои данные ✅")
async def bot_start(message: types.Message):
    # cupid.dump_users()
    # cupid.dump_questionnaires()
    # user = db.get_user(message.from_user.id)
    # candidates = cupid.find_candidate(user)
    # if len(candidates):
    #     await message.answer(
    #         text=f"Найден кандидат:\n"
    #              f"Имя: {candidates[0].get('name')}\n"
    #              f"Юзернейм: {candidates[0].get('username')}"
    #     )
    # print(candidates)
    user = db.get_user(message.from_user.id)
    db.update_known_users(message.from_user.id, '893534')
    message_text = create_message_by_user_questionnaire(user)
    await message.answer(message_text, parse_mode="HTML")



