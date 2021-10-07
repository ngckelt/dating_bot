from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.main_markup import main_markup
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from loader import dp
from utils.cities.cities import check_city
from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire_markup
from .utils import create_message_by_user_questionnaire, is_correct_age_range, create_message_by_search_questionnaire, \
    is_correct_age
from states.change_search_questionnarie import ChangeSearchQuestionnaire
from .utils import prepare_answers, translate_choice
from keyboards.inline.user_questionare_markup import *


@dp.message_handler(text="Изменить данные для поиска 📝")
async def change_search_data(message: types.Message):
    try:
        user = db.get_user(message.from_user.id)
        q = db.get_questionnaire_by_user(user)
        message_text = create_message_by_search_questionnaire(q)
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        await message.answer(message_text)
        await message.answer(
            text="Что Вы хотите изменить?",
            reply_markup=change_search_questionnaire_markup()
        )
        await ChangeSearchQuestionnaire.chose_item.set()
    except AttributeError:
        await message.answer("Чтобы воспользоваться ботом, Вам сперва необходимо заполнить анкеты")


MIN_AGE_ID = "1"
MAX_AGE_ID = "2"
NATIONALITY_ID = "3"
EDUCATION_ID = "4"
EDUCATION_CITY_ID = "5"
CITY_ID = "6"
HAS_CAR_ID = "7"
HAS_OWN_HOUSING_ID = "8"
PROFESSION_ID = "9"
MARITAL_STATUS_ID = "10"
HAS_CHILDREN_ID = "11"


@dp.callback_query_handler(change_user_data_callback.filter(), state=ChangeSearchQuestionnaire.chose_item)
async def get_change_item(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    item = callback_data.get('item')
    # Диапазон возраста
    if item == 'age_range':
        await callback.message.answer(text="Укажите новый минимальный возраст")
        await ChangeSearchQuestionnaire.change_min_age.set()
    # Национальность
    elif item == 'nationality':
        question = db.get_search_question_by_id(NATIONALITY_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите национальность из списка",
            reply_markup=nationality_markup(answers)
        )
        await ChangeSearchQuestionnaire.change_nationality.set()
    # Образование
    elif item == 'education':
        question = db.get_search_question_by_id(EDUCATION_ID)
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
    # Город образования
    elif item == 'education_city':
        question = db.get_search_question_by_id(EDUCATION_CITY_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите город, где получали образование",
            reply_markup=universal_markup(
                answers,
                'education_city_callback',
            )
        )
        await ChangeSearchQuestionnaire.change_education_city.set()
    # Город
    elif item == 'city':
        question = db.get_search_question_by_id(CITY_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите город текущего проживания",
            reply_markup=universal_markup(
                answers,
                'city_callback',
            )
        )
        await ChangeSearchQuestionnaire.change_city.set()
    # Чем должен заниматься
    elif item == 'profession':
        question = db.get_search_question_by_id(PROFESSION_ID)
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
    # Семейное положение
    elif item == 'marital_status':
        question = db.get_search_question_by_id(MARITAL_STATUS_ID)
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
    # Есть ли автомобиль
    elif item == 'has_car':
        await callback.message.answer(
            text="Должен ли быть автомобиль",
            reply_markup=yes_or_no_markup('has_car', does_not_matter=True)
        )
        await ChangeSearchQuestionnaire.change_has_car.set()
    # Есть ли собственное жилье
    elif item == 'has_own_housing':
        await callback.message.answer(
            text="Должно ли быть собственное жилье",
            reply_markup=yes_or_no_markup('has_own_housing', does_not_matter=True)
        )
        await ChangeSearchQuestionnaire.change_has_own_housing.set()
    # Есть ли дети
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
        # Тут можно сделать вывод новой анкеты
        user = db.get_user(callback.from_user.id)
        q = db.get_questionnaire_by_user(user)
        message_text = create_message_by_search_questionnaire(q)
        await callback.message.answer(message_text)
        await state.finish()


# Меняем минимальный возросат
@dp.message_handler(state=ChangeSearchQuestionnaire.change_min_age)
async def change_min_age(message: types.Message, state: FSMContext):
    check = is_correct_age(message.text)
    if check.get('correct'):
        await state.update_data(min_age=message.text)
        await message.answer(text="Укажите максимальный возраст")
        await ChangeSearchQuestionnaire.change_max_age.set()
    else:
        await message.answer(check.get('message'))


# Меняем максимальный возраст
@dp.message_handler(state=ChangeSearchQuestionnaire.change_max_age)
async def change_max_age(message: types.Message, state: FSMContext):
    check = is_correct_age(message.text)
    if check.get('correct'):
        state_data = await state.get_data()
        if int(message.text) > int(state_data.get('min_age')):
            user = db.get_user(message.from_user.id)
            age_range = f"{state_data.get('min_age')} {message.text}"
            db.update_search_questionnaire(user, age_range=age_range)
            await ask_to_continue_changing(message)
        else:
            await message.answer("Максимальный возраст должен быть больше минимального")
    else:
        await message.answer(check.get('message'))


# Смена национальности (кнопка)
@dp.callback_query_handler(nationality_callback.filter(), state=ChangeSearchQuestionnaire.change_nationality)
async def change_nationality(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    nationalities = state_data.get('answers')
    nationality_index = callback_data.get('nationality')
    chosen_nationality = nationalities[int(nationality_index)]
    if chosen_nationality == "Иное (указать)\r":
        await callback.message.answer("Укажите национаьность")
        await ChangeSearchQuestionnaire.change_nationality_by_message.set()
    else:
        user = db.get_user(callback.from_user.id)
        db.update_search_questionnaire(user, nationality=chosen_nationality)
        await ask_to_continue_changing(callback.message)


@dp.message_handler(state=ChangeSearchQuestionnaire.change_nationality_by_message)
async def change_nationality_by_message(message: types.Message, state: FSMContext):
    nationality = message.text.capitalize()
    user = db.get_user(message.from_user.id)
    db.update_search_questionnaire(user, nationality=nationality)
    await ask_to_continue_changing(message)


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
    if int(education_city_index) == len(educations) - 1:
        await callback.message.answer("Укажите город")
        await ChangeSearchQuestionnaire.change_education_city_by_message.set()
    else:
        chosen_education_city = educations[int(education_city_index)]
        user = db.get_user(callback.from_user.id)
        db.update_search_questionnaire(user, education_city=chosen_education_city)
        await ask_to_continue_changing(callback.message)


# Изменить город образования (сообщения)
@dp.message_handler(state=ChangeSearchQuestionnaire.change_education_city_by_message)
async def change_education_city_by_message(message: types.Message, state: FSMContext):
    education_city = message.text
    check = check_city(education_city)
    if check.get('equal'):
        user = db.get_user(message.from_user.id)
        db.update_search_questionnaire(user, education_city=message.text)
        await ask_to_continue_changing(message)
    elif check.get('candidate'):
        await state.update_data(education_city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имели в виду {check.get('candidate')}?",
            reply_markup=yes_or_no_markup('change_education_city')
        )
        await ChangeSearchQuestionnaire.change_education_city_candidate.set()
    else:
        await message.answer("Не удалось распознать город")


# Город образования (кандидат)
@dp.callback_query_handler(yes_or_no_callback.filter(question='change_education_city'),
                           state=ChangeSearchQuestionnaire.change_education_city_candidate)
async def get_education_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        user = db.get_user(callback.from_user.id)
        print(state_data.get('education_city_candidate'))
        db.update_search_questionnaire(user, education_city=state_data.get('education_city_candidate'))
        await ask_to_continue_changing(callback.message)
    else:
        await callback.message.answer("Укажите город еще раз")
        await ChangeSearchQuestionnaire.change_education_city_by_message.set()


# Город проживания (кнопка)
@dp.callback_query_handler(city_callback.filter(), state=ChangeSearchQuestionnaire.change_city)
async def get_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    cities = state_data.get('answers')
    city_index = callback_data.get('city')
    if int(city_index) == len(cities) - 1:
        await callback.message.answer("Укажите город")
        await ChangeSearchQuestionnaire.change_city_by_message.set()
    else:
        chosen_city = cities[int(city_index)]
        user = db.get_user(callback.from_user.id)
        db.update_search_questionnaire(user, city=chosen_city)
        await ask_to_continue_changing(callback.message)


# Город проживания (сообщение)
@dp.message_handler(state=ChangeSearchQuestionnaire.change_city_by_message)
async def change_city_by_message(message: types.Message, state: FSMContext):
    city = message.text
    check = check_city(city)
    if check.get('equal'):
        user = db.get_user(message.from_user.id)
        db.update_search_questionnaire(user, city=city)
        await ask_to_continue_changing(message)
    elif check.get('candidate'):
        await state.update_data(city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имели в виду {check.get('candidate')}?",
            reply_markup=yes_or_no_markup('change_city')
        )
        await ChangeSearchQuestionnaire.change_city_candidate.set()
    else:
        await message.answer("Не удалось распознать город")


# Город проживания (кандидат)
@dp.callback_query_handler(yes_or_no_callback.filter(question='change_city'),
                           state=ChangeSearchQuestionnaire.change_city_candidate)
async def get_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        user = db.get_user(callback.from_user.id)
        db.update_search_questionnaire(user, city=state_data.get('city_candidate'))
        await ask_to_continue_changing(callback.message)
    else:
        await callback.message.answer("Укажите город еще раз")
        await ChangeSearchQuestionnaire.change_city_by_message.set()


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


@dp.message_handler(state=ChangeSearchQuestionnaire)
async def chose_item_error(message: types.Message, state: FSMContext):
    await message.answer(text="Пожалуйста, выберите один из предоставленных пунктов")



