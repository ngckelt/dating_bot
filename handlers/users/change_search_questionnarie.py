from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from loader import dp

from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire
from .utils import create_message_by_user_questionnaire, is_correct_age_range, create_message_by_search_questionnaire
from keyboards.inline.user_questionare_markup import \
    change_search_questionnaire_markup, change_user_data_callback
from states.change_search_questionnarie import ChangeSearchQuestionnaire


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


@dp.callback_query_handler(change_user_data_callback.filter(), state=ChangeSearchQuestionnaire.chose_item)
async def get_change_item(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    item = callback_data.get('item')
    if item == 'age_range':
        await callback.message.answer(text="Укажите новый возрастной диапазон")
        await ChangeSearchQuestionnaire.change_age.set()
    elif item == 'nationality':
        await callback.message.answer(text="Выберите национальность из списка")
        await ChangeSearchQuestionnaire.change_nationality.set()
        await state.finish()
    elif item == 'education':
        await callback.message.answer(text="Выбарите уровень образования")
        await ChangeSearchQuestionnaire.change_education.set()
        await state.finish()
    elif item == 'education_city':
        await callback.message.answer(text="Укажите еород, где получали образование")
        await ChangeSearchQuestionnaire.change_education_city.set()
        await state.finish()
    elif item == 'city':
        await callback.message.answer(text="Укажите город текущего проживания")
        await ChangeSearchQuestionnaire.change_city.set()
        await state.finish()
    elif item == 'profession':
        await callback.message.answer(text="Укажите новый вид деятельности")
        await ChangeSearchQuestionnaire.change_profession.set()
        await state.finish()
    elif item == 'marital_status':
        await callback.message.answer(text="Выберите семейное положение")
        await ChangeSearchQuestionnaire.change_marital_status.set()
        await state.finish()
    elif item == 'has_car':
        await callback.message.answer(text="Должен ли быть автомобиль")
        await ChangeSearchQuestionnaire.change_has_car.set()
        await state.finish()
    elif item == 'has_own_housing':
        await callback.message.answer(text="Должно ли быть собственное жилье")
        await ChangeSearchQuestionnaire.change_has_own_housing.set()
    elif item == 'has_children':
        await callback.message.answer(text="Могут ли быть дети")
        await ChangeSearchQuestionnaire.change_has_children.set()
        await state.finish()


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


@dp.message_handler(state=ChangeSearchQuestionnaire.chose_item)
async def chose_item_error(message: types.Message, state: FSMContext):
    await message.answer(
        text="Пожалуйста, выберите один из вариантов ответа"
    )