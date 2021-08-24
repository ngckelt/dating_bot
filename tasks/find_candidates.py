from asyncio import sleep
from datetime import datetime
from pprint import pprint

from utils.db_api import botdb as db
from utils.cupid import cupid
from loader import bot
import aioschedule


async def search_candidates():
    print("search_start")
    users = db.get_users()
    questionnaires = db.get_questionnaires()
    cupid.dump_users(users)
    cupid.dump_questionnaires(questionnaires)

    for user in users:
        user_candidate = cupid.find_candidate(user)
        if user_candidate:
            known_users = user.known_users['known_users']
            if user_candidate.get('telegram_id') not in known_users:
                user_name = user_candidate.get('username')
                if not user_name:
                    user_name = "Не указан"
                message = "Найден кандидат!\n" \
                          f"Имя: {user_candidate.get('name')}\n" \
                          f"Юзернейм: {user_name}\n"
                db.update_known_users(
                    user,
                    user_candidate.get('telegram_id')
                )
                try:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=message
                    )
                except Exception as e:
                    print(e)
    cupid.clear_dumps()
    print("search_end")


async def setup():
    print("task start")
    aioschedule.every().day.at("20:22").do(search_candidates)

    while True:
        await aioschedule.run_pending()
        await sleep(100)

