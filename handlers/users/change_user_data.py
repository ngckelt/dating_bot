from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from loader import dp

from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from .utils import create_message_by_user_questionnaire


@dp.message_handler(text="Изменить данные")
async def bot_start(message: types.Message):
    await message.answer("Это еще не делал")
