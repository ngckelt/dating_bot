from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.questionnaire_markups import fill_search_questionnaire
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
        "no": "Нет",
        "does_not_matter": "Не имеет значения"
    }.get(choice)


# Имя
@dp.message_handler(text="Заполнить анкету о себе ✅")
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


# Имя
@dp.message_handler(state=FillUserQuestionnaire.get_name)
async def get_name(message: types.Message, state: FSMContext):
    # Добавить пару проверок на входные данные
    state_data = await state.get_data()
    name = message.text
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(name=name, current_question=current_question)
    # Спрашиваем возраст
    await message.answer(text=questions[current_question-1].question)
    await FillUserQuestionnaire.get_age.set()


# Возраст
@dp.message_handler(state=FillUserQuestionnaire.get_age)
async def get_age(message: types.Message, state: FSMContext):
    age = message.text
    try:
        age = int(age)
        if 18 <= age <= 70:
            state_data = await state.get_data()
            questions = state_data.get('questions')
            current_question = state_data.get('current_question')
            current_question += 1
            await state.update_data(age=age, current_question=current_question)
            answers = prepare_answers(questions[current_question - 1].answer_options)
            # Спрашиваем национальность
            await state.update_data(nationalities=answers)
            await message.answer(
                text=f"Ворос {current_question}/11\n{questions[current_question-1].question}",
                reply_markup=nationality_markup(answers)
            )
            await FillUserQuestionnaire.get_nationality.set()
        else:
            await message.answer("Возраст должен находиться в диапазоне от 18 до 70")
    except ValueError:
        await message.answer("Воздаст должен быть указан числом")


# Национальность (кнопка)
@dp.callback_query_handler(nationality_callback.filter(), state=FillUserQuestionnaire.get_nationality)
async def get_nationality(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    nationality = callback_data.get('nationality')
    nationalities = state_data.get('nationalities')
    if int(nationality) == len(nationalities) - 1:
        await callback.message.answer(text="Укажите вашу национальность")
    else:
        nationality = nationalities[int(nationality)]
        await state.update_data(nationalities=None)
        questions = state_data.get('questions')
        current_question = state_data.get('current_question')
        current_question += 1
        await state.update_data(nationality=nationality, current_question=current_question)
        answers = prepare_answers(questions[current_question - 1].answer_options)
        await callback.message.answer(
            # Спрашиваем образование
            text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
            reply_markup=universal_markup(answers, 'education_callback')
        )
        await FillUserQuestionnaire.get_education.set()


# Национальность (сообщение)
@dp.message_handler(state=FillUserQuestionnaire.get_nationality)
async def get_nationality_by_message(message: types.Message, state: FSMContext):
    nationality = message.text
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(nationality=nationality, current_question=current_question)
    await message.answer(
        # Спрашиваем образование
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[current_question - 1].answer_options),
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
    educations = questions[current_question-1].answer_options.split('\n')
    current_question += 1
    education = educations[int(education_index)]

    await state.update_data(education=education, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем город, где получал образование
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[current_question - 1].answer_options),
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
    education_cities = questions[current_question-1].answer_options.split('\n')
    if int(education_city_index) == len(education_cities) - 1:
        await callback.message.answer(text="Укажите город, в котором вы получали образование")
    else:
        current_question += 1
        education_city = education_cities[int(education_city_index)]
        await state.update_data(education_city=education_city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем город текущкго проживания
            text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
            reply_markup=universal_markup(
                prepare_answers(questions[current_question - 1].answer_options),
                'city_callback'
            )
        )
        await FillUserQuestionnaire.get_city.set()


@dp.message_handler(state=FillUserQuestionnaire.get_education_city)
async def get_education_city_message(message: types.Message, state: FSMContext):
    education_city = message.text
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(education_city=education_city, current_question=current_question)
    await message.answer(
        # Спрашиваем город текущкго проживания
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[current_question - 1].answer_options),
            'city_callback'
        )
    )
    await FillUserQuestionnaire.get_city.set()


# Город проживания
@dp.callback_query_handler(city_callback.filter(), state=FillUserQuestionnaire.get_city)
async def get_city(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    city_index = callback_data.get('city')
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    cities = questions[current_question - 1].answer_options.split('\n')
    if int(city_index) == len(cities) - 1:
        await callback.message.answer(text="Укажите город, в котором вы сейчас проживаете")
    else:
        current_question += 1
        city = cities[int(city_index)]
        await state.update_data(city=city, current_question=current_question)
        await callback.message.answer(
            # Спрашиваем есть ли автомобиль
            text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
            reply_markup=yes_or_no_markup('has_car')
        )
        await FillUserQuestionnaire.has_car.set()
        
        
@dp.message_handler(state=FillUserQuestionnaire.get_city)
async def get_city_message(message: types.Message, state: FSMContext):
    city = message.text
    state_data = await state.get_data()
    questions = state_data.get('questions')
    current_question = state_data.get('current_question')
    current_question += 1
    await state.update_data(city=city, current_question=current_question)
    await message.answer(
        # Спрашиваем есть ли автомобиль
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
        reply_markup=yes_or_no_markup('has_car')
    )
    await FillUserQuestionnaire.has_car.set()

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
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
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
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[current_question - 1].answer_options),
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
    professions = questions[current_question - 1].answer_options.split('\n')
    current_question += 1
    profession = professions[int(profession_index)]
    await state.update_data(profession=profession, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем семейное положение
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
        reply_markup=universal_markup(
            prepare_answers(questions[current_question - 1].answer_options),
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
    marital_statuses = questions[current_question - 1].answer_options.split('\n')
    current_question += 1
    marital_status = marital_statuses[int(marital_status_index)]
    await state.update_data(marital_status=marital_status, current_question=current_question)
    await callback.message.answer(
        # Спрашиваем есть ли дети
        text=f"Ворос {current_question}/11\n{questions[current_question - 1].question}",
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
        name=state_data.get('name'),
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
    user_data = f"Имя: {user.name}\n" \
                f"Возраст: {user.age}\n" \
                f"Национальность: {user.nationality}\n" \
                f"Образование: {user.education}\n" \
                f"Город, где получали образование: {user.education_city}\n" \
                f"Город текущего проживания: {user.city}\n" \
                f"Есть автомобиль: {user.has_car}\n" \
                f"Есть собственное жилье: {user.has_own_housing}\n" \
                f"Профессия: {user.profession}\n" \
                f"Семейное положение: {user.marital_status}\n" \
                f"Есть дети: {user.has_children}"
    await callback.message.answer(
        text=f"Ваши данные:\n{user_data}"
    )

    await callback.message.answer(
        text="Теперь Вам необходимо заполнить анкету для поиска",
        reply_markup=fill_search_questionnaire()
    )
    await state.finish()






