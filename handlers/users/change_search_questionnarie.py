from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.main_markup import main_markup
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from loader import dp
from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from .utils import create_message_by_user_questionnaire, is_correct_age_range, create_message_by_search_questionnaire
from states.change_search_questionnarie import ChangeSearchQuestionnaire
from .utils import prepare_answers, translate_choice
from keyboards.inline.user_questionare_markup import *


@dp.message_handler(text="Изменить данные для поиска")
async def bot_start(message: types.Message):
    user = db.get_user(message.from_user.id)
    q = db.get_questionnaire_by_user(user)
    message_text = create_message_by_search_questionnaire(q)
    await message.answer(message_text)
    await message.answer(
        text="Что Вы хотите изменить?",
        reply_markup=change_search_questionnaire_markup()
    )
    await ChangeSearchQuestionnaire.chose_item.set()

"""
Возраст - 1
Национальность - 2
Образование - 3
Город образования - 4
Город проживания - 5
Должен ли быть автомобиль - 6
Жилье - 7
Занятие - 8
Семейное положение - 9
Дети - 10
"""


@dp.callback_query_handler(change_user_data_callback.filter(), state=ChangeSearchQuestionnaire.chose_item)
async def get_change_item(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    item = callback_data.get('item')
    if item == 'age_range':
        await callback.message.answer(text="Укажите новый возрастной диапазон")
        await ChangeSearchQuestionnaire.change_age.set()
    elif item == 'nationality':
        question = db.get_search_question_by_id("2")
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите национальность из списка",
            reply_markup=nationality_markup(answers)
        )
        await ChangeSearchQuestionnaire.change_nationality.set()
    elif item == 'education':
        question = db.get_search_question_by_id("3")
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите уровень образования",
            reply_markup=universal_markup(
                answers,
                'education_callback'
            )
        )
        await ChangeSearchQuestionnaire.change_education.set()
    elif item == 'education_city':
        question = db.get_search_question_by_id("4")
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите город, где получали образование",
            reply_markup=universal_markup(
                answers,
                'education_city_callback',
                does_not_matter=True
            )
        )
        await ChangeSearchQuestionnaire.change_education_city.set()
    elif item == 'city':
        question = db.get_search_question_by_id("5")
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите город текущего проживания",
            reply_markup=universal_markup(
                answers,
                'city_callback',
                does_not_matter=True
            )
        )
        await ChangeSearchQuestionnaire.change_city.set()
    elif item == 'profession':
        question = db.get_search_question_by_id("8")
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите новый вид деятельности",
            reply_markup=universal_markup(
                answers,
                'profession_callback',
                does_not_matter=True
            )
        )
        await ChangeSearchQuestionnaire.change_profession.set()
    elif item == 'marital_status':
        question = db.get_search_question_by_id("9")
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите семейное положение",
            reply_markup=universal_markup(
                answers,
                'marital_status_callback'
            )
        )
        await ChangeSearchQuestionnaire.change_marital_status.set()
    elif item == 'has_car':
        await callback.message.answer(
            text="Должен ли быть автомобиль",
            reply_markup=yes_or_no_markup('has_car', does_not_matter=True)
        )
        await ChangeSearchQuestionnaire.change_has_car.set()
    elif item == 'has_own_housing':
        await callback.message.answer(
            text="Должно ли быть собственное жилье",
            reply_markup=yes_or_no_markup('has_own_housing', does_not_matter=True)
        )
        await ChangeSearchQuestionnaire.change_has_own_housing.set()
    elif item == 'has_children':
        await callback.message.answer(
            text="Могут ли быть дети",
            reply_markup=yes_or_no_markup('has_children')
        )
        await ChangeSearchQuestionnaire.change_has_children.set()


async def ask_to_continue_changing(message):
    await message.answer(
        text="Хотите изменить что-то еще?",
        reply_markup=yes_or_no_markup("continue_changing")
    )
    await ChangeSearchQuestionnaire.change_item.set()


@dp.callback_query_handler(yes_or_no_callback.filter(question='continue_changing'),
                           state=ChangeSearchQuestionnaire.change_item)
async def continue_changing(callback: types.CallbackQuery, callback_data: dict,
                            state: FSMContext):
    await callback.answer()
    if callback_data.get('choice') == 'yes':
        await callback.message.answer(
            text="Что Вы хотите изменить?",
            reply_markup=change_search_questionnaire_markup()
        )
        await ChangeSearchQuestionnaire.chose_item.set()
    else:
        await callback.message.answer("Данные успешно изменены")
        # user = db.get_user(callback.message.from_user.id)
        # q = db.get_questionnaire_by_user(user)
        # message_text = create_message_by_search_questionnaire(q)
        # await callback.message.answer(message_text)
        await state.finish()


@dp.message_handler(state=ChangeSearchQuestionnaire.change_age)
async def change_age_range(message: types.Message, state: FSMContext):
    check = is_correct_age_range(message.text)
    if check.get('correct'):
        user = db.get_user(message.from_user.id)
        n1, n2 = check.get('n1'), check.get('n2')
        db.update_search_questionnaire(user, age_range=f"{n1} {n2}")
        await ask_to_continue_changing(message)
    else:
        await message.answer(check.get('message'))


# Смена национальности
@dp.callback_query_handler(nationality_callback.filter(), state=ChangeSearchQuestionnaire.change_nationality)
async def change_nationality(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    nationalities = state_data.get('answers')
    nationality_index = callback_data.get('nationality')
    chosen_nationality = nationalities[int(nationality_index)]
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, nationality=chosen_nationality)
    await ask_to_continue_changing(callback.message)


# Образование (кнопка)
@dp.callback_query_handler(education_callback.filter(), state=ChangeSearchQuestionnaire.change_education)
async def get_education(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    educations = state_data.get('answers')
    education_index = callback_data.get('education')
    chosen_education = educations[int(education_index)]
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, education=chosen_education)
    await ask_to_continue_changing(callback.message)


# Город образования (кнопка)
@dp.callback_query_handler(education_city_callback.filter(), state=ChangeSearchQuestionnaire.change_education_city)
async def get_education_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    educations = state_data.get('answers')
    education_city_index = callback_data.get('education_city')
    if education_city_index == '-1':
        chosen_education_city = "Не имеет значения"
    else:
        chosen_education_city = educations[int(education_city_index)]
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, education_city=chosen_education_city)
    await ask_to_continue_changing(callback.message)


# Город проживания (кнопка)
@dp.callback_query_handler(city_callback.filter(), state=ChangeSearchQuestionnaire.change_city)
async def get_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    cities = state_data.get('answers')
    city_index = callback_data.get('city')
    if city_index == '-1':
        chosen_city = "Не имеет значения"
    else:
        chosen_city = cities[int(city_index)]
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, city=chosen_city)
    await ask_to_continue_changing(callback.message)


# Профессия
@dp.callback_query_handler(profession_callback.filter(), state=ChangeSearchQuestionnaire.change_profession)
async def get_profession(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    professions = state_data.get('answers')
    profession_index = callback_data.get('profession')
    if profession_index == '-1':
        chosen_profession = "Не имеет значения"
    else:
        chosen_profession = professions[int(profession_index)]
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, profession=chosen_profession)
    await ask_to_continue_changing(callback.message)


# Семейное положение
@dp.callback_query_handler(marital_status_callback.filter(), state=ChangeSearchQuestionnaire.change_marital_status)
async def get_marital_status(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    marital_statuses = state_data.get('answers')
    status_index = callback_data.get('marital_status')
    chosen_status = marital_statuses[int(status_index)]
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, marital_status=chosen_status)
    await ask_to_continue_changing(callback.message)


# Есть ли тачка
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_car'), state=ChangeSearchQuestionnaire.change_has_car)
async def has_car(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, has_car=translate_choice(choice))
    await ask_to_continue_changing(callback.message)


# Есть ли собственное жилье
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_own_housing'),
                           state=ChangeSearchQuestionnaire.change_has_own_housing)
async def has_own_housing(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, has_own_housing=translate_choice(choice))
    await ask_to_continue_changing(callback.message)


# Могут ли быть дети
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_children'),
                           state=ChangeSearchQuestionnaire.change_has_children)
async def has_children(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    user = db.get_user(callback.from_user.id)
    db.update_search_questionnaire(user, has_children=translate_choice(choice))
    await ask_to_continue_changing(callback.message)


@dp.message_handler(state=ChangeSearchQuestionnaire.chose_item)
async def chose_item_error(message: types.Message, state: FSMContext):
    await message.answer(
        text="Пожалуйста, выберите один из вариантов ответа"
    )