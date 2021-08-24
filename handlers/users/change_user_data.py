import calendar

from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.user_questionare_markup import *
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from keyboards.default.main_markup import main_markup
from utils.cities.cities import check_city
from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from states.change_user_data import ChangeUserData
from utils.db_api import botdb as db
from .utils import *


NAME_ID = '1'
AGE_ID = '2'
NATIONALITY_ID = '3'
EDUCATION_ID = '4'
EDUCATION_CITY_ID = '5'
CITY_ID = '6'
HAS_CAR_ID = '7'
HOUSING_ID = '8'
PROFESSION_ID = '9'
MARITAL_STATUS_ID = '10'
HAS_CHILDREN_ID = '11'
GENDER_ID = '12'


async def ask_to_continue_changing(message):
    await message.answer(
        text="Хотите изменить что-то еще?",
        reply_markup=yes_or_no_markup("continue_changing")
    )
    await ChangeUserData.change_item.set()


@dp.message_handler(text="Изменить данные о себе ✏️")
async def update_user_data(message: types.Message):
    try:
        user = db.get_user(message.from_user.id)
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        user_data_text = create_message_by_user_questionnaire(user)
        await message.answer(user_data_text)
        await message.answer(
            text="Что Вы хотите изменить?",
            reply_markup=change_user_data_markup()
        )
        await ChangeUserData.chose_item.set()
    except AttributeError:
        await message.answer("Чтобы воспользоваться ботом, Вам необходимо заполнить анкеты")


@dp.callback_query_handler(yes_or_no_callback.filter(question='continue_changing'),
                           state=ChangeUserData.change_item)
async def continue_changing(callback: types.CallbackQuery, callback_data: dict,
                            state: FSMContext):
    await callback.answer()
    if callback_data.get('choice') == 'yes':
        await callback.message.answer(
            text="Что Вы хотите изменить?",
            reply_markup=change_user_data_markup()
        )
        await ChangeUserData.chose_item.set()
    else:
        await callback.message.answer("Данные успешно изменены")
        user = db.get_user(callback.from_user.id)
        message_text = create_message_by_user_questionnaire(user)
        await callback.message.answer(message_text)
        await state.finish()


@dp.callback_query_handler(change_user_data_callback.filter(), state=ChangeUserData.chose_item)
async def get_change_item(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    item = callback_data.get('item')
    if item == 'name':
        await callback.message.answer(text="Укажите новое имя")
        await ChangeUserData.change_name.set()
    if item == 'gender':
        question = db.get_user_question_by_id(GENDER_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите пол",
            reply_markup=universal_markup(
                answers,
                'gender_callback'
            )
        )
        await ChangeUserData.change_gender.set()
    elif item == 'age':
        await callback.message.answer(text="Укажите новый возраст")
        await ChangeUserData.change_age.set()
    elif item == 'nationality':
        question = db.get_user_question_by_id(NATIONALITY_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите национальность из списка",
            reply_markup=nationality_markup(answers)
        )
        await ChangeUserData.change_nationality.set()
    elif item == 'education':
        question = db.get_user_question_by_id(EDUCATION_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите уровень образования",
            reply_markup=universal_markup(
                answers,
                'education_callback'
            )
        )
        await ChangeUserData.change_education.set()
    # Город образования
    elif item == 'education_city':
        question = db.get_user_question_by_id(EDUCATION_CITY_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите город, где получали образование",
            reply_markup=universal_markup(
                answers,
                'education_city_callback',
            )
        )
        await ChangeUserData.change_education_city.set()
    # Город проживания
    elif item == 'city':
        question = db.get_user_question_by_id(CITY_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите город текущего проживания",
            reply_markup=universal_markup(
                answers,
                'city_callback',
            )
        )
        await ChangeUserData.change_city.set()
    elif item == 'profession':
        question = db.get_user_question_by_id(PROFESSION_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Укажите новый вид деятельности",
            reply_markup=universal_markup(
                answers,
                'profession_callback',
            )
        )
        await ChangeUserData.change_profession.set()
    elif item == 'marital_status':
        question = db.get_user_question_by_id(MARITAL_STATUS_ID)
        answers = prepare_answers(question.answer_options)
        await state.update_data(answers=answers)
        await callback.message.answer(
            text="Выберите семейное положение",
            reply_markup=universal_markup(
                answers,
                'marital_status_callback'
            )
        )
        await ChangeUserData.change_marital_status.set()
    elif item == 'has_car':
        await callback.message.answer(
            text="Есть ли автомобиль",
            reply_markup=yes_or_no_markup('has_car')
        )
        await ChangeUserData.change_has_car.set()
    elif item == 'has_own_housing':
        await callback.message.answer(
            text="Есть ли собственное жилье",
            reply_markup=yes_or_no_markup('has_own_housing')
        )
        await ChangeUserData.change_has_own_housing.set()
    elif item == 'has_children':
        await callback.message.answer(
            text="Есть ли дети",
            reply_markup=yes_or_no_markup('has_children')
        )
        await ChangeUserData.change_has_children.set()


# Меняем имя
@dp.message_handler(state=ChangeUserData.change_name)
async def change_name(message: types.Message, state: FSMContext):
    name = message.text
    # user = db.get_user(message.from_user.id)
    db.update_user(message.from_user.id, name=name)
    await ask_to_continue_changing(message)


# Меняем пол
@dp.callback_query_handler(gender_callback.filter(), state=ChangeUserData.change_gender)
async def change_gender(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    genders = state_data.get('answers')
    gender_index = callback_data.get('gender')
    gender = genders[int(gender_index)]
    db.update_user(callback.from_user.id, gender=gender)
    await ask_to_continue_changing(callback.message)


# Меняем возраст
@dp.message_handler(state=ChangeUserData.change_age)
async def change_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age in range(18, 71):
            db.update_user(message.from_user.id, age=age)
            await ask_to_continue_changing(message)
        else:
            await message.answer("Возраст должен быть в диапазоне 18-70")
    except ValueError:
        await message.answer("Возраст должен быть указан целым числом")


# Меняем национальность
@dp.callback_query_handler(nationality_callback.filter(), state=ChangeUserData.change_nationality)
async def change_nationality(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    nationalities = state_data.get('answers')
    nationality_index = callback_data.get('nationality')
    if int(nationality_index) == len(nationalities) - 1:
        await callback.message.answer("Укажите вашу национальность")
    else:
        chosen_nationality = nationalities[int(nationality_index)]
        db.update_user(callback.from_user.id, nationality=chosen_nationality)
        await ask_to_continue_changing(callback.message)


# Меняем национальность с помощью сообщения
@dp.message_handler(state=ChangeUserData.change_nationality)
async def change_nationality_by_message(message: types.Message, state: FSMContext):
    nationality = message.text
    db.update_user(message.from_user.id, nationality=nationality)
    await ask_to_continue_changing(message)


# Меняем образование
@dp.callback_query_handler(education_callback.filter(), state=ChangeUserData.change_education)
async def change_education(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    educations = state_data.get('answers')
    education_index = callback_data.get('education')
    chosen_education = educations[int(education_index)]
    db.update_user(callback.from_user.id, education=chosen_education)
    await ask_to_continue_changing(callback.message)


# Меняем город образования
@dp.callback_query_handler(education_city_callback.filter(), state=ChangeUserData.change_education_city)
async def get_education_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    educations = state_data.get('answers')
    education_city_index = callback_data.get('education_city')
    pprint(education_city_index)
    if int(education_city_index) == len(educations) - 1:
        await callback.message.answer("Укажите город, в котором Вы получали образование")
    else:
        chosen_education_city = educations[int(education_city_index)]
        db.update_user(callback.from_user.id, education_city=chosen_education_city)
        await ask_to_continue_changing(callback.message)


# Меняем город образования (сообщение)
@dp.message_handler(state=ChangeUserData.change_education_city)
async def change_education_city_message(message: types.Message, state: FSMContext):
    education_city = message.text
    check = check_city(education_city)
    if check.get('equal'):
        db.update_user(message.from_user.id, education_city=education_city)
        await ask_to_continue_changing(message)
    elif check.get('candidate'):
        await state.update_data(education_city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имели в виду {check.get('candidate')}",
            reply_markup=yes_or_no_markup('education_city_candidate')
        )
    else:
        await message.answer("Неудалось распознать город. Попробуйте еще раз")


# Меняем горд образования (кандидат)
@dp.callback_query_handler(yes_or_no_callback.filter(question='education_city_candidate'),
                           state=ChangeUserData.change_education_city)
async def education_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        db.update_user(callback.from_user.id, education_city=state_data.get('education_city_candidate'))
        await ask_to_continue_changing(callback.message)
    else:
        await callback.message.answer("Укажите город еще раз")


# Меняем город проживания
@dp.callback_query_handler(city_callback.filter(), state=ChangeUserData.change_city)
async def get_education_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    educations = state_data.get('answers')
    education_city_index = callback_data.get('city')
    if int(education_city_index) == len(educations) - 1:
        await callback.message.answer("Укажите город, в котором Вы проживаете")
    else:
        chosen_education_city = educations[int(education_city_index)]
        db.update_user(callback.from_user.id, city=chosen_education_city)
        await ask_to_continue_changing(callback.message)


# Меняем город проживания (сообщение)
@dp.message_handler(state=ChangeUserData.change_city)
async def change_city_by_message(message: types.Message, state: FSMContext):
    city = message.text
    check = check_city(city)
    if check.get('equal'):
        db.update_user(message.from_user.id, city=city)
        await ask_to_continue_changing(message)
    elif check.get('candidate'):
        await state.update_data(city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имели в виду {check.get('candidate')}?",
            reply_markup=yes_or_no_markup('city_candidate')
        )


@dp.callback_query_handler(yes_or_no_callback.filter(question='city_candidate'), state=ChangeUserData.change_city)
async def change_city_by_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        db.update_user(callback.from_user.id, city=state_data.get('city_candidate'))
        await ask_to_continue_changing(callback.message)
    else:
        await callback.message.answer("Укажите город еще раз")


# Меняем профессию
@dp.callback_query_handler(profession_callback.filter(), state=ChangeUserData.change_profession)
async def get_profession(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    professions = state_data.get('answers')
    profession_index = callback_data.get('profession')
    chosen_profession = professions[int(profession_index)]
    db.update_user(callback.from_user.id, profession=chosen_profession)
    await ask_to_continue_changing(callback.message)


# Меняем семейное положение
@dp.callback_query_handler(marital_status_callback.filter(), state=ChangeUserData.change_marital_status)
async def get_marital_status(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    marital_statuses = state_data.get('answers')
    status_index = callback_data.get('marital_status')
    chosen_status = marital_statuses[int(status_index)]
    db.update_user(callback.from_user.id, marital_status=chosen_status)
    await ask_to_continue_changing(callback.message)


# Есть ли тачка
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_car'), state=ChangeUserData.change_has_car)
async def has_car(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    db.update_user(callback.from_user.id, has_car=translate_choice(choice))
    await ask_to_continue_changing(callback.message)


# Есть ли собственное жилье
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_own_housing'),
                           state=ChangeUserData.change_has_own_housing)
async def has_own_housing(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    db.update_user(callback.from_user.id, has_own_housing=translate_choice(choice))
    await ask_to_continue_changing(callback.message)


# Есть ли дети
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_children'),
                           state=ChangeUserData.change_has_children)
async def has_children(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    db.update_user(callback.from_user.id, has_children=translate_choice(choice))
    await ask_to_continue_changing(callback.message)







