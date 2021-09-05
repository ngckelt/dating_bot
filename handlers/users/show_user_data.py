from aiogram import types
from loader import dp
from keyboards.inline.link_to_user_markup import user_data_callback
from utils.db_api.botdb import get_waiting_questionnaire


@dp.callback_query_handler(user_data_callback.filter())
async def show_user_data(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    user_data_id = callback_data.get('user_data_id')
    q = get_waiting_questionnaire(user_data_id)
    if q is not None:
        await callback.message.answer(q.text)
    else:
        await callback.message.answer("Данные отсутствуют")




