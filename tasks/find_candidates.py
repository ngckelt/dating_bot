from asyncio import sleep
from datetime import datetime
from pprint import pprint

from keyboards.inline.link_to_user_markup import link_to_user_markup
from utils.db_api import botdb as db
from utils.cupid import cupid
from loader import bot

from handlers.users.utils import create_candidate_data_message, create_user_data_message
import aioschedule


async def search_candidates():
    users = db.get_users()
    questionnaires = db.get_questionnaires()
    cupid.dump_users(users)
    cupid.dump_questionnaires(questionnaires)

    for user in users:
        candidates = cupid.find_candidates(user)
        if candidates:
            known_users = user.known_users['known_users']
            for candidate in candidates:
                if candidate.get('telegram_id') not in known_users:
                    to_user_markup = None
                    to_candidate_markup = None
                    if candidate.get('username'):
                        # to_user_markup = link_to_user_markup(candidate.get('username'))
                        to_user_markup = link_to_user_markup(candidate.get('username'))
                    if user.username:
                        to_candidate_markup = link_to_user_markup(user.username)
                        # to_candidate_markup = link_to_user_markup('larwyn')
                    candidate_data_message = create_candidate_data_message(candidate)
                    user_data_message = create_user_data_message(user)
                    db.update_known_users(
                        user,
                        candidate.get('telegram_id')
                    )
                    try:
                        # Сообщение пользователю, для которого нашелся кандидат
                        await bot.send_message(
                            chat_id=user.telegram_id,
                            text=candidate_data_message,
                            reply_markup=to_user_markup
                        )
                    except Exception as e:
                        print(e)
                    try:
                        # Сообщение для пользователя, которого выбрали кандидатом
                        await bot.send_message(
                            chat_id=candidate.get('telegram_id'),
                            text=user_data_message,
                            reply_markup=None
                        )
                    except Exception as e:
                        print(e)
                    break
    cupid.clear_dumps()


async def setup():
    aioschedule.every().day.at("14:00").do(search_candidates)

    while True:
        await aioschedule.run_pending()
        await sleep(10)

