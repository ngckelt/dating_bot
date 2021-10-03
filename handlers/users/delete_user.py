from aiogram import types
from loader import dp
from keyboards.inline.confirm_markup import confirm_markup, confirm_callback
from utils.db_api import botdb as db


@dp.message_handler(text="Удалить мои данные ❌️")
async def delete_user(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user is not None:
        if message.from_user.username:
            db.update_user(message.from_user.id, username=message.from_user.username)
        await message.answer(
            text="Внимание! Ваши данные будут удалены без воможности восстановления. Продолжить?",
            reply_markup=confirm_markup('delete_user')
        )
    else:
        await message.answer("Чтобы воспользоваться ботом, Вам необходимо заполнить анкеты")


@dp.callback_query_handler(confirm_callback.filter(question="delete_user"))
async def confirm_delete_suer(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'True':
        db.delete_user(callback.from_user.id)
        await callback.message.answer(
            text="Данные успешно удалены",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await callback.message.answer("Действие отменено")

