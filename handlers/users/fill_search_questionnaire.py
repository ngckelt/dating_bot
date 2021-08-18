from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.fill_user_questionnaire import FillUserQuestionnaire
from utils.db_api import botdb as db
from keyboards.inline.user_questionare_markup import *
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback


def prepare_answers(answers):
    answers = answers.split('\n')
    return answers


def translate_choice(choice):
    return {
        "yes": "Да",
        "no": "Нет"
    }.get(choice)


# Имя
@dp.message_handler(text="Заполнить анкету для поиска ✅")
async def bot_start(message: types.Message, state: FSMContext):
    questions = db.get_user_questions()
    current_question = 1
    await state.update_data(questions=questions, current_question=current_question)
    await message.answer(
        # Спрашиваем имя
        text=f"Вопрос {current_question}/11\n{questions[current_question-1].question}",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await FillUserQuestionnaire.get_name.set()
