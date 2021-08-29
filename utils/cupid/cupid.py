import json
import os
from pprint import pprint

from utils.db_api import botdb as db

USERS_DATA_PATH = 'utils/cupid/users.json'
QUESTIONNAIRES_PATH = 'utils/cupid/questionnaires.json'
DOES_NOT_MATTER = "Не имеет значения"


def dump(file_path, data):
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, default=str))


def dump_users(users):
    users_data = dict()
    for user in users:
        users_data[user.telegram_id] = user.__dict__
    dump(USERS_DATA_PATH, users_data)


def dump_questionnaires(questionnaires):
    questionnaires_data = dict()
    for q in questionnaires:
        questionnaires_data[q.user.telegram_id] = q.__dict__
    dump(QUESTIONNAIRES_PATH, questionnaires_data)


def get_candidates():
    with open(USERS_DATA_PATH) as f:
        data = json.loads(f.read())
    return data


def prepare_data(candidate_data):
    for key, value in candidate_data.items():
        if isinstance(value, str):
            candidate_data[key] = value.replace('\r', '')
    return candidate_data


def calculate_match_percentage(candidate, questionnaire, user):
    candidate = prepare_data(candidate)
    questionnaire = prepare_data(questionnaire)
    # Проверить что это не сам пользователь
    if candidate.get('telegram_id') == user.telegram_id:
        return 0
    # print('not yourself', end=" ")
    # Активен ли для поиска
    if not candidate.get('active_to_search'):
        return 0
    # print('active', end=" ")
    # Пол
    if candidate.get('gender') == user.gender:
        return 0
    # print('gender', end=" ")
    # Проверить возраст
    user_age = candidate.get('age')
    desired_min_age, desired_max_age = questionnaire.get('age_range').split()
    if int(user_age) not in range(int(desired_min_age), int(desired_max_age) + 1):
        return 0
    # print('age', end=" ")
    # Город
    if candidate.get('city') != questionnaire.get('city'):
        return 0
    # print('city', end=" ")
    # Образование
    if candidate.get('education') != questionnaire.get('education'):
        return 0
    # print('education', end=" ")
    # Город образования
    if candidate.get('education_city') != questionnaire.get('education_city'):
        return 0
    # print('education city', end=" ")
    # Есть ли тачка
    if questionnaire.get('has_car') != DOES_NOT_MATTER:
        if candidate.get('has_car') != questionnaire.get('has_car'):
            return 0
    # print('car', end=" ")
    # Могут ли быть дети
    if questionnaire.get('has_children') == 'Нет':
        if candidate.get('has_children') != questionnaire.get('has_children'):
            return 0
    # print('children', end=" ")
    # Есть ли жилье
    if questionnaire.get('has_own_housing') != DOES_NOT_MATTER:
        if candidate.get('has_own_housing') != questionnaire.get('has_own_housing'):
            return 0
    # print('housing', end=" ")
    # Семейное положение
    if candidate.get('marital_status') != questionnaire.get('marital_status'):
        return 0
    # print('marital', end=" ")
    # Национальность
    if questionnaire.get('nationality') != DOES_NOT_MATTER:
        if candidate.get('nationality') != questionnaire.get('nationality'):
            return 0
    # print('nationality', end=" ")
    # Профессия
    if questionnaire.get('profession') != DOES_NOT_MATTER:
        if candidate.get('profession') != questionnaire.get('profession'):
            return 0
    # print('profession', end=" ")
    print("******* Кандидат найден *******")
    return 1


def get_candidates_by_questionnaire(questionnaire, user):
    print(f"Ищем кандидата для: {user.username}\n")
    candidates = []
    users = get_candidates()
    for candidate_id, candidate_data in users.items():
        if calculate_match_percentage(candidate_data, questionnaire, user):
            candidates.append(candidate_data)
    return candidates


def get_user_questionnaire(user_telegram_id):
    with open(QUESTIONNAIRES_PATH) as f:
        questionnaires = json.loads(f.read())
    return questionnaires.get(user_telegram_id)


def get_best_candidates(user):
    q = get_user_questionnaire(user.telegram_id)
    candidates = None
    if q is not None:
        candidates = get_candidates_by_questionnaire(q, user)
    return candidates


def find_candidates(user):
    candidate = get_best_candidates(user)
    return candidate


def clear_dumps():
    os.remove(USERS_DATA_PATH)
    os.remove(QUESTIONNAIRES_PATH)



