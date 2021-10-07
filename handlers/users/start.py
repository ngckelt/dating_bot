from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_markup import main_markup
from loader import dp

from utils.db_api import botdb as db
from keyboards.default.questionnaire_markups import fill_user_questionnaire_markup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user is None:
        if message.from_user.username is None:
            await message.answer("Внимание ❗️\nУ Вас не указано Имя пользователя в настройках Telegram. "
                                 "Оно необходимо, чтобы другие пользователи "
                                 "бота могли Вас найти. Установите его, а после еще раз воспользуйтесь командой "
                                 "/start, чтобы зарегистрироваться в боте")

        else:
            await message.answer(
                text=f"Приветствуем Вас, {message.from_user.first_name}! 👋\n"
                     f"Чтобы воспользоваться ботом, Вам сперва необходимо заполнить "
                     f"анкету с данными о себе. Чтобы сделать это, воспользуйтесь кнопкой ниже 👇",
                reply_markup=fill_user_questionnaire_markup()
            )
    else:
        await message.answer(
            text="Вы уже использовали данную команду",
            reply_markup=main_markup()
        )


