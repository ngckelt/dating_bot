import ctypes
from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.questionnaire_markups import fill_search_questionnaire, fill_user_questionnaire as fill_user_questionnaire_markup
from loader import dp
from states.fill_user_questionnaire import FillUserQuestionnaire
from utils.db_api import botdb as db
from keyboards.inline.user_questionare_markup import *
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from keyboards.default.questionnaire_markups import cancel_fill_markup
from utils.cities.cities import check_city
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


@dp.message_handler(text="Заполнить анкету заново 🔄", state=FillUserQuestionnaire)
async def reset_fill(message: types.Message, state: FSMContext):
    await state.finish()
    questions = db.get_user_questions()
    current_question = 1
    await state.update_data(questions=questions, current_question=current_question)
    await message.answer(
        # Спрашиваем имя
        text=f"Вопрос {current_question}/12\n{questions[NAME_ID].question}",
        reply_markup=cancel_fill_markup()
    )
    await FillUserQuestionnaire.get_name.set()


@dp.message_handler(text="Отменить заполнение анкеты ❌", state=FillUserQuestionnaire)
async def cancel_fill(message: types.Message, state: FSMContext):
    await message.answer(
        text="Заполнение анкеты отменено. Вы можоте вернуться к заполнению анкеты в удобное для Вас время, "
             "еще раз нажав кнопку ниже",
        reply_markup=fill_user_questionnaire_markup()
    )
    await state.finish()


# Начало
@dp.message_handler(text="Заполнить анкету о себе 📝")
async def fill_user_questionnaire(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if user is None:
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        questions = db.get_user_questions()
        current_question = 1
        await state.update_data(questions=questions, current_question=current_question)
        await message.answer(
            # Спрашиваем имя
            text=f"Вопрос {current_question}/12\n{questions[NAME_ID].question}",
            reply_markup=cancel_fill_markup()
        )
        await FillUserQuestionnaire.get_name.set()
    else:
        await message.answer("У Вас уже есть заполненная анкета")


# Имя
@dp.message_handler(state=FillUserQuestionnaire.get_name)
async def get_name(message: types.Message, state: FSMContext):
    # Добавить пару проверок на входные данные
    state_data = await state.get_data()
    name = message.text
    check = check_name(name)
    if check['name']:
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(name=check['name'], current_question=current_question)
        # Спрашиваем пол
        await message.answer(
            text=f"Вопрос {current_question}/12\n{questions[GENDER_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[GENDER_ID].answer_options),
                'gender_callback'
            )
        )
        await FillUserQuestionnaire.get_gender.set()
    else:
        await message.answer(check['message'])


# Пол
@dp.callback_query_handler(gender_callback.filter(), state=FillUserQuestionnaire.get_gender)
async def get_gender(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    genders = questions[GENDER_ID].answer_options.split('\n')
    gender_index = callback_data.get('gender')
    chosen_gender = genders[int(gender_index)]
    current_question += 1
    await state.update_data(gender=chosen_gender, current_question=current_question)
    # Спрашиваем возраст
    await callback.message.answer(
        text=f"Вопрос {current_question}/12\n{questions[AGE_ID].question}",
    )
    await FillUserQuestionnaire.get_age.set()


# Возраст
@dp.message_handler(state=FillUserQuestionnaire.get_age)
async def get_age(message: types.Message, state: FSMContext):
    age = message.text
    check = is_correct_age(age)
    if check.get('correct'):
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(age=age, current_question=current_question)
        answers = prepare_answers(questions[NATIONALITY_ID].answer_options)
        # Спрашиваем национальность
        await state.update_data(nationalities=answers)
        await message.answer(
            text=f"Вопрос {current_question}/12\n{questions[NATIONALITY_ID].question}",
            reply_markup=nationality_markup(answers)
        )
        await FillUserQuestionnaire.get_nationality.set()
    else:
        await message.answer(check['message'])


# Национальность (кнопка)
@dp.callback_query_handler(nationality_callback.filter(), state=FillUserQuestionnaire.get_nationality)
async def get_nationality(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    nationality = callback_data.get('nationality')
    nationalities = state_data.get('nationalities')
    if int(nationality) == len(nationalities) - 1:
        await callback.message.answer(text="Укажите вашу национальность")
        await FillUserQuestionnaire.get_nationality_by_message.set()
    else:
        nationality = nationalities[int(nationality)]
        await state.update_data(nationalities=None)
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(nationality=nationality, current_question=current_question)
        answers = prepare_answers(questions[EDUCATION_ID].answer_options)
        await callback.message.answer(
            # Спрашиваем образование
            text=f"Вопрос {current_question}/12\n{questions[EDUCATION_ID].question}",
            reply_markup=universal_markup(answers, 'education_callback')
        )
        await FillUserQuestionnaire.get_education.set()


# Национальность (сообщение)
@dp.message_handler(state=FillUserQuestionnaire.get_nationality_by_message)
async def get_nationality_by_message(message: types.Message, state: FSMContext):
    nationality = message.text
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(nationality=nationality, current_question=current_question)
    await message.answer(
        # Спрашиваем образование
        text=f"Вопрос {current_question}/12\n{questions[EDUCATION_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[EDUCATION_ID].answer_options),
            'education_callback'
        )
    )
    await FillUserQuestionnaire.get_education.set()


# Образование (кнопка)
@dp.callback_query_handler(education_callback.filter(), state=FillUserQuestionnaire.get_education)
async def get_education(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    education_index = callback_data.get('education')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    educations = questions[EDUCATION_ID].answer_options.split('\n')
    current_question += 1
    education = educations[int(education_index)]

    await state.update_data(education=education, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем город, где получал образование
        text=f"Вопрос {current_question}/12\n{questions[EDUCATION_CITY_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[EDUCATION_CITY_ID].answer_options),
            'education_city_callback'
        )
    )
    await FillUserQuestionnaire.get_education_city.set()


# Город, где получал образование (кнопка)
@dp.callback_query_handler(education_city_callback.filter(), state=FillUserQuestionnaire.get_education_city)
async def get_education_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    education_city_index = callback_data.get('education_city')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    education_cities = questions[EDUCATION_CITY_ID].answer_options.split('\n')
    if int(education_city_index) == len(education_cities) - 1:
        await callback.message.answer(text="Укажите город, в котором вы получали образование")
        await FillUserQuestionnaire.get_education_city_by_message.set()
    else:
        current_question += 1
        education_city = education_cities[int(education_city_index)]
        await state.update_data(education_city=education_city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Вопрос {current_question}/12\n{questions[CITY_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[CITY_ID].answer_options),
                'city_callback'
            )
        )
        await FillUserQuestionnaire.get_city.set()


# Город, где получали образование (сообщение)
@dp.message_handler(state=FillUserQuestionnaire.get_education_city_by_message)
async def get_education_city_message(message: types.Message, state: FSMContext):
    education_city = message.text
    check = check_city(education_city)
    if check.get('equal'):
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(education_city=education_city, current_question=current_question)
        await message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Вопрос {current_question}/12\n{questions[CITY_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[CITY_ID].answer_options),
                'city_callback'
            )
        )
        await FillUserQuestionnaire.get_city.set()
    elif check.get('candidate'):
        await state.update_data(city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имели в виду {check.get('candidate')}?",
            reply_markup=yes_or_no_markup('education_city')
        )
        await FillUserQuestionnaire.get_education_city_candidate.set()
    else:
        await message.answer("Не удалось распознать ваш город. Попробуйте еще раз")


# Город образования (кандидат)
@dp.callback_query_handler(yes_or_no_callback.filter(question='education_city'),
                           state=FillUserQuestionnaire.get_education_city_candidate)
async def get_education_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(education_city=state_data.get('city_candidate'), current_question=current_question)
        await callback.message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Вопрос {current_question}/12\n{questions[CITY_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[CITY_ID].answer_options),
                'city_callback'
            )
        )
        await FillUserQuestionnaire.get_city.set()
    else:
        await callback.message.answer("Укажите Ваш город еще раз")
        await FillUserQuestionnaire.get_education_city_by_message.set()


# Город проживания (кнопка)
@dp.callback_query_handler(city_callback.filter(), state=FillUserQuestionnaire.get_city)
async def get_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    city_index = callback_data.get('city')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    cities = questions[CITY_ID].answer_options.split('\n')
    if int(city_index) == len(cities) - 1:
        await callback.message.answer(text="Укажите город, в котором вы сейчас проживаете")
        await FillUserQuestionnaire.get_city_by_message.set()
    else:
        current_question += 1
        city = cities[int(city_index)]
        await state.update_data(city=city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем есть ли автомобиль
            text=f"Вопрос {current_question}/12\n{questions[HAS_CAR_ID].question}",
            reply_markup=yes_or_no_markup('has_car')
        )
        await FillUserQuestionnaire.has_car.set()


# Город (сообщение)
@dp.message_handler(state=FillUserQuestionnaire.get_city_by_message)
async def get_city_message(message: types.Message, state: FSMContext):
    city = message.text.capitalize()
    city_data = check_city(city)
    if city_data['equal']:
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(city=city, current_question=current_question)
        await message.answer(
            # Спрашиваем есть ли автомобиль
            text=f"Вопрос {current_question}/12\n{questions[HAS_CAR_ID].question}",
            reply_markup=yes_or_no_markup('has_car')
        )
        await FillUserQuestionnaire.has_car.set()
    elif city_data['candidate'] is not None:
        # Уточняем город
        await state.update_data(city_candidate=city_data['candidate'])
        await message.answer(
            text=f"Возможно, вы имели в виду {city_data['candidate']}?",
            reply_markup=yes_or_no_markup('city_candidate')
        )
        await FillUserQuestionnaire.get_city_candidate.set()
    else:
        await message.answer("Не удалось распознать Ваш город. Попробуйте еще раз")


# Проверка города (сообщение)
@dp.callback_query_handler(yes_or_no_callback.filter(question='city_candidate'),
                           state=FillUserQuestionnaire.get_city_candidate)
async def get_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(city=state_data.get('city_candidate'), current_question=current_question)
        await callback.message.answer(
            # Спрашиваем есть ли автомобиль
            text=f"Вопрос {current_question}/12\n{questions[HAS_CAR_ID].question}",
            reply_markup=yes_or_no_markup('has_car')
        )
        await FillUserQuestionnaire.has_car.set()
    else:
        await callback.message.answer(text="Укажите Ваш город еще раз")
        await FillUserQuestionnaire.get_city_by_message.set()


# Есть ли машина (кнопка)
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_car'), state=FillUserQuestionnaire.has_car)
async def has_car(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    has_car = callback_data.get('choice')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(has_car=has_car, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем есть ли собственное жилье
        text=f"Вопрос {current_question}/12\n{questions[HOUSING_ID].question}",
        reply_markup=yes_or_no_markup('has_own_housing')
    )
    await FillUserQuestionnaire.has_own_housing.set()


# Есть ли жилье (кнопка)
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_own_housing'),
                           state=FillUserQuestionnaire.has_own_housing)
async def has_own_housing(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    has_own_housing = callback_data.get('choice')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(has_own_housing=has_own_housing, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем чем сейчас занимается
        text=f"Вопрос {current_question}/12\n{questions[PROFESSION_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[PROFESSION_ID].answer_options),
            'profession_callback'
        )
    )
    await FillUserQuestionnaire.get_profession.set()


# Профессия (кнопка)
@dp.callback_query_handler(profession_callback.filter(), state=FillUserQuestionnaire.get_profession)
async def get_profession(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    profession_index = callback_data.get('profession')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    professions = questions[PROFESSION_ID].answer_options.split('\n')
    current_question += 1
    profession = professions[int(profession_index)]
    await state.update_data(profession=profession, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем семейное положение
        text=f"Вопрос {current_question}/12\n{questions[MARITAL_STATUS_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[MARITAL_STATUS_ID].answer_options),
            'marital_status_callback'
        )
    )
    await FillUserQuestionnaire.get_marital_status.set()


# Семейное положение (кнопка)
@dp.callback_query_handler(marital_status_callback.filter(), state=FillUserQuestionnaire.get_marital_status)
async def get_marital_status(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    marital_status_index = callback_data.get('marital_status')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    marital_statuses = questions[MARITAL_STATUS_ID].answer_options.split('\n')
    current_question += 1
    marital_status = marital_statuses[int(marital_status_index)]
    await state.update_data(marital_status=marital_status, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем есть ли дети
        text=f"Вопрос {current_question}/12\n{questions[HAS_CHILDREN_ID].question}",
        reply_markup=yes_or_no_markup('has_children')
    )
    await FillUserQuestionnaire.has_children.set()


# Есть ли дети (кнопка)
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_children'),
                           state=FillUserQuestionnaire.has_children)
async def has_children(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    has_children = callback_data.get('choice')
    db.add_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        name=state_data.get('name'),
        gender=state_data.get('gender'),
        age=state_data.get('age'),
        nationality=state_data.get('nationality'),
        education=state_data.get('education'),
        education_city=state_data.get('education_city'),
        city=state_data.get('city'),
        profession=state_data.get('profession'),
        marital_status=state_data.get('marital_status'),
        has_car=translate_choice(state_data.get('has_car')),
        has_own_housing=translate_choice(state_data.get('has_own_housing')),
        has_children=translate_choice(has_children),
    )
    user = db.get_user(callback.from_user.id)
    user_data_test = create_message_by_user_questionnaire(user)
    await callback.message.answer(
        text=user_data_test
    )

    await callback.message.answer(
        text="Теперь Вам необходимо заполнить анкету для поиска",
        reply_markup=fill_search_questionnaire()
    )
    await state.finish()


# Ловим сообщения, когда нужно нажать на кнопку
@dp.message_handler(state=FillUserQuestionnaire)
async def catch_message(message: types.Message):
    await message.answer("Пожалуйста, выберите один из предоставленных пунктов")

