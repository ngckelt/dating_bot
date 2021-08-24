from aiogram import types
from loader import dp
from keyboards.inline.user_questionare_markup import change_search_status_markup, change_search_status_callback
from utils.db_api import botdb as db


@dp.message_handler(text="Изменить статус для поиска 🖌️")
async def change_user_search_status(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user is not None:
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        await message.answer(
            text="Выберите статус",
            reply_markup=change_search_status_markup()
        )
    else:
        await message.answer("Чтобы воспользоваться ботом, Вам необходимо заполнить анкеты")


@dp.callback_query_handler(change_search_status_callback.filter())
async def confirm_change_search_status(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    status = callback_data.get('status')
    if status == 'active':
        db.change_user_search_status(callback.from_user.id, True)
    else:
        db.change_user_search_status(callback.from_user.id, False)
    await callback.message.answer("Данные успешно изменены")

