from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_markup import main_markup
from keyboards.default.questionnaire_markups import cancel_fill_markup, fill_search_questionnaire
from loader import dp
from states.fill_search_questionnaire import FillSearchQuestionnaire
from utils.db_api import botdb as db
from keyboards.inline.user_questionare_markup import *
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from .utils import *
from utils.cities.cities import check_city

MIN_AGE_ID = '1'
MAX_AGE_ID = '2'
NATIONALITY_ID = '3'
EDUCATION_ID = '4'
EDUCATION_CITY_ID = '5'
CITY_ID = '6'
HAS_CAR_ID = '7'
HAS_OWN_HOUSING_ID = '8'
PROFESSION_ID = '9'
MARITAL_STATUS_ID = '10'
HAS_CHILDREN_ID = '11'


@dp.message_handler(text="Заполнить анкету заново 🔄", state=FillSearchQuestionnaire)
async def reset_fill(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    questionnaire = db.get_questionnaire_by_user(user)
    if not questionnaire:
        questions = db.get_search_questions()
        current_question = 1
        await state.update_data(questions=questions, current_question=current_question)
        # Спрашиваем минимальный возраст
        await message.answer(
            text=f"Ворос {current_question}/11\n{questions[MIN_AGE_ID].question}",
            reply_markup=cancel_fill_markup()
        )
        await FillSearchQuestionnaire.get_min_age.set()
    else:
        await message.answer("У вас уже есть заполненная анкета")


@dp.message_handler(text="Отменить заполнение анкеты ❌", state=FillSearchQuestionnaire)
async def cancel_fill(message: types.Message, state: FSMContext):
    await message.answer(
        text="Заполнение анкеты отменено. Вы можоте вернуться к заполнению анкеты в удобное для Вас время, "
             "еще раз нажав кнопку ниже",
        reply_markup=fill_search_questionnaire()
    )
    await state.finish()


# Начало
@dp.message_handler(text="Заполнить анкету для поиска 📝")
async def bot_start(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    questionnaire = db.get_questionnaire_by_user(user)
    if not questionnaire:
        questions = db.get_search_questions()
        current_question = 1
        await state.update_data(questions=questions, current_question=current_question)
        # Спрашиваем минимальный возраст
        await message.answer(
            text=f"Ворос {current_question}/11\n{questions[MIN_AGE_ID].question}",
            reply_markup=cancel_fill_markup()
        )
        await FillSearchQuestionnaire.get_min_age.set()
    else:
        await message.answer("У вас уже есть заполненная анкета")


# Минимальный возраст
@dp.message_handler(state=FillSearchQuestionnaire.get_min_age)
async def get_min_age(message: types.Message, state: FSMContext):
    age = message.text
    check = is_correct_age(age)
    if check['correct']:
        state_data = await state.get_data()
        current_question = state_data.get('current_question')
        await state.update_data(min_age=age)
        questions = db.get_search_questions()
        current_question += 1
        await state.update_data(current_question=current_question)
        await message.answer(text=f"Вопрос {current_question}/11\n{questions[MAX_AGE_ID].question}")
        await FillSearchQuestionnaire.get_max_age.set()
    elif check['message']:
        await message.answer(text=check['message'])


# Максимальный возраст
@dp.message_handler(state=FillSearchQuestionnaire.get_max_age)
async def get_max_age(message: types.Message, state: FSMContext):
    age = message.text
    check = is_correct_age(age)
    if check['correct']:
        state_data = await state.get_data()
        if int(age) < int(state_data.get('min_age')):
            await message.answer("Максимальный возраст должен быть больше минимального")
        else:
            await state.update_data(max_age=age)
            questions = state_data.get('questions')
            current_question = state_data.get('current_question')
            current_question += 1
            answers = prepare_answers(questions[NATIONALITY_ID].answer_options)
            await state.update_data(current_question=current_question, nationalities=answers)
            # Спрашиваем национальность
            await message.answer(
                text=f"Ворос {current_question}/11\n{questions[NATIONALITY_ID].question}",
                reply_markup=nationality_markup(answers)
            )
            await FillSearchQuestionnaire.get_nationality.set()

    elif check['message']:
        await message.answer(text=check['message'])


# Национальность (кнопка)
@dp.callback_query_handler(nationality_callback.filter(), state=FillSearchQuestionnaire.get_nationality)
async def get_nationality(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    nationality = callback_data.get('nationality')
    nationalities = state_data.get('nationalities')
    nationality = nationalities[int(nationality)]
    await state.update_data(nationalities=None)
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(nationality=nationality, current_question=current_question)
    answers = prepare_answers(questions[EDUCATION_ID].answer_options)
    await callback.message.answer(
        # Спрашиваем образование
        text=f"Ворос {current_question}/11\n{questions[EDUCATION_ID].question}",
        reply_markup=universal_markup(answers, 'education_callback')
    )
    await FillSearchQuestionnaire.get_education.set()


# Образование (кнопка)
@dp.callback_query_handler(education_callback.filter(), state=FillSearchQuestionnaire.get_education)
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
        text=f"Ворос {current_question}/11\n{questions[EDUCATION_CITY_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[EDUCATION_CITY_ID].answer_options),
            'education_city_callback'
        )
    )
    await FillSearchQuestionnaire.get_education_city.set()


# Город, где получал образование (кнопка)
@dp.callback_query_handler(education_city_callback.filter(), state=FillSearchQuestionnaire.get_education_city)
async def get_education_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    education_city_index = callback_data.get('education_city')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    education_cities = questions[EDUCATION_CITY_ID].answer_options.split('\n')
    current_question += 1
    if int(education_city_index) == len(education_cities) - 1:
        # Просим ввести город самостоятельно
        await callback.message.answer(text="Укажите город")
    else:
        education_city = education_cities[int(education_city_index)]
        await state.update_data(education_city=education_city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Ворос {current_question}/11\n{questions[CITY_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[CITY_ID].answer_options),
                'city_callback',
            )
        )
        await FillSearchQuestionnaire.get_city.set()


# Город, где получали образование (сообщение)
@dp.message_handler(state=FillSearchQuestionnaire.get_education_city)
async def get_education_city_by_message(message: types.Message, state: FSMContext):
    city = message.text
    check = check_city(city)
    if check.get('equal'):
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        education_city = city.capitalize()
        await state.update_data(education_city=education_city, current_question=current_question)
        await message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Ворос {current_question}/11\n{questions[CITY_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[CITY_ID].answer_options),
                'city_callback',
            )
        )
        await FillSearchQuestionnaire.get_city.set()
    elif check.get('candidate'):
        await state.update_data(city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имель в виду {check.get('candidate')}?",
            reply_markup=yes_or_no_markup('city_candidate')
        )
    else:
        await message.answer("Не удалось расознать Ваш город. Попробуйте еще раз")


# Город где получали образование (кандидат)
@dp.callback_query_handler(yes_or_no_callback.filter(question='city_candidate'),
                           state=FillSearchQuestionnaire.get_education_city)
async def get_education_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        city = state_data.get('city_candidate')
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        education_city = city.capitalize()
        await state.update_data(education_city=education_city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Ворос {current_question}/11\n{questions[CITY_ID].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[CITY_ID].answer_options),
                'city_callback',
            )
        )
        await FillSearchQuestionnaire.get_city.set()
    else:
        await callback.message.answer("Укажите город еще раз")


# Город проживания
@dp.callback_query_handler(city_callback.filter(), state=FillSearchQuestionnaire.get_city)
async def get_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    city_index = callback_data.get('city')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    cities = questions[CITY_ID].answer_options.split('\n')
    current_question += 1
    if int(city_index) == len(cities) - 1:
        await callback.message.answer("Укажите город")
    else:
        city = cities[int(city_index)]
        await state.update_data(city=city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем должен ли быть автомобиль
            text=f"Ворос {current_question}/11\n{questions[HAS_CAR_ID].question}",
            reply_markup=yes_or_no_markup('has_car', does_not_matter=True)
        )
        await FillSearchQuestionnaire.has_car.set()


# Город проживания (сообщение)
@dp.message_handler(state=FillSearchQuestionnaire.get_city)
async def get_city_by_message(message: types.Message, state: FSMContext):
    city = message.text
    check = check_city(city)
    if check.get('equal'):
        state_data = await state.get_data()
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        living_city = city.capitalize()
        await state.update_data(city=living_city, current_question=current_question)
        await message.answer(
            # Спрашиваем должен ли быть автомобиль
            text=f"Ворос {current_question}/11\n{questions[HAS_CAR_ID].question}",
            reply_markup=yes_or_no_markup('has_car', does_not_matter=True)
        )
        await FillSearchQuestionnaire.has_car.set()
    elif check.get('candidate'):
        await state.update_data(city_candidate=check.get('candidate'))
        await message.answer(
            text=f"Возможно, Вы имель в виду {check.get('candidate')}?",
            reply_markup=yes_or_no_markup('city')
        )
    else:
        await message.answer("Не удалось расознать Ваш город. Попробуйте еще раз")


# Город проживания (кандидат)
@dp.callback_query_handler(yes_or_no_callback.filter(question='city'), state=FillSearchQuestionnaire.get_city)
async def get_city_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        state_data = await state.get_data()
        city = state_data.get('city_candidate')
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        living_city = city.capitalize()
        await state.update_data(city=living_city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем должен ли быть автомобиль
            text=f"Ворос {current_question}/11\n{questions[HAS_CAR_ID].question}",
            reply_markup=yes_or_no_markup('has_car', does_not_matter=True)
        )
        await FillSearchQuestionnaire.has_car.set()
    else:
        await callback.message.answer("Укажите город еще раз")


# Должна ли быть машина
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_car'), state=FillSearchQuestionnaire.has_car)
async def has_car(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    has_car = callback_data.get('choice')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(has_car=has_car, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем должно ли быть собственное жилье
        text=f"Ворос {current_question}/11\n{questions[HAS_OWN_HOUSING_ID].question}",
        reply_markup=yes_or_no_markup('has_own_housing', does_not_matter=True)
    )
    await FillSearchQuestionnaire.has_own_housing.set()


# Есть ли жилье (кнопка)
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_own_housing'),
                           state=FillSearchQuestionnaire.has_own_housing)
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
        text=f"Ворос {current_question}/11\n{questions[PROFESSION_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[PROFESSION_ID].answer_options),
            'profession_callback',
            does_not_matter=True
        )
    )
    await FillSearchQuestionnaire.get_profession.set()


# Профессия (кнопка)
@dp.callback_query_handler(profession_callback.filter(), state=FillSearchQuestionnaire.get_profession)
async def get_profession(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    profession_index = callback_data.get('profession')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    professions = questions[PROFESSION_ID].answer_options.split('\n')
    current_question += 1
    if int(profession_index) == -1:
        profession = "Не имеет значения"
    else:
        profession = professions[int(profession_index)]
    await state.update_data(profession=profession, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем семейное положение
        text=f"Ворос {current_question}/11\n{questions[MARITAL_STATUS_ID].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[MARITAL_STATUS_ID].answer_options),
            'marital_status_callback'
        )
    )
    await FillSearchQuestionnaire.get_marital_status.set()


# Семейное положение (кнопка)
@dp.callback_query_handler(marital_status_callback.filter(), state=FillSearchQuestionnaire.get_marital_status)
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
        # Спрашиваем могут ли быть дети
        text=f"Ворос {current_question}/11\n{questions[HAS_CHILDREN_ID].question}",
        reply_markup=yes_or_no_markup('has_children')
    )
    await FillSearchQuestionnaire.has_children.set()


# Есть ли дети (кнопка)
@dp.callback_query_handler(yes_or_no_callback.filter(question='has_children'),
                           state=FillSearchQuestionnaire.has_children)
async def has_children(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    has_children = callback_data.get('choice')
    user = db.get_user(callback.from_user.id)
    db.create_questionnaire(
        user=user,
        age_range=f"{state_data.get('min_age')}  {state_data.get('max_age')}",
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

    questionnaire = db.get_questionnaire_by_user(user)
    questionnaire_text = create_message_by_search_questionnaire(questionnaire)
    await callback.message.answer(
        questionnaire_text,
        reply_markup=main_markup()
    )
    await state.finish()





