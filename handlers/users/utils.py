from pprint import pprint
import re


def prepare_answers(answers):
    answers = answers.split('\n')
    return answers


def translate_choice(choice):
    return {
        "yes": "Да",
        "no": "Нет",
        "does_not_matter": "Не имеет значения"
    }.get(choice)


def is_correct_age(age):
    response = {'correct': False, 'message': None}
    try:
        age = int(age)
        if age in range(18, 71):
            response['correct'] = True
        else:
            response['message'] = "Возраст должен быть в диапазоне от 18 до 70"
    except ValueError:
        response['message'] = "Возраст должен быть указан целым числом"
    return response


def is_correct_age_range(age_range):
    correct = False
    error_message = ""
    n1, n2 = 0, 0
    try:
        n1, n2 = age_range.split()
        try:
            n1, n2 = int(n1), int(n2)
            if n1 < n2:
                if n1 in range(18, 71) and n2 in range(18, 71):
                    correct = True
                else:
                    error_message = "Оба числа должны быть в диапазоне от 18 до 70"
            else:
                error_message = "Первое число должно быть меньше второго"
        except ValueError:
            error_message = "Значения должны быть указаны целыми числами"
    except ValueError:
        error_message = "Должно быть указано 2 числа"

    return {'correct': correct, 'message': error_message, 'n1': n1, 'n2': n2}


def create_message_by_user_questionnaire(user):
    search_status = "Да"
    status_emoji = "🟢"
    if not user.active_to_search:
        search_status = "Нет"
        status_emoji = "🔴"
    if user.gender == "Мужской\r":
        gender_emoji = "🙎‍♂️"
    else:
        gender_emoji = "🙍‍♀️"
    message = f"Ваши данные:\n\n" \
              f"{status_emoji} Активен для поиска: <b>{search_status}</b>\n\n" \
              f"🆔 Юзернейм: <b>{user.username}</b>\n\n" \
              f"🆗 Имя: <b>{user.name}</b>\n\n" \
              f"{gender_emoji} Пол: <b>{user.gender}</b>\n\n" \
              f"✅ Возраст: <b>{user.age}\n\n</b>" \
              f"🏳️ Национальность: <b>{user.nationality}</b>\n\n" \
              f"🎓 Образование: <b>{user.education}</b>\n\n" \
              f"🏙 Город, где получали образование: <b>{user.education_city}</b>\n\n" \
              f"🌆 Город текущего проживания: <b>{user.city}</b>\n\n" \
              f"🚗 Есть автомобиль: <b>{user.has_car}</b>\n\n" \
              f"🏡 Есть собственное жилье: <b>{user.has_own_housing}</b>\n\n" \
              f"💼 Род деятельности: <b>{user.profession}</b>\n\n" \
              f"💍 Семейное положение: <b>{user.marital_status}</b>\n\n" \
              f"👶 Есть дети: <b>{user.has_children}</b>"
    return message


def create_message_by_search_questionnaire(questionnaire):
    message = f"📋 Ваша анкета для поиска:\n\n" \
              f"✅ Диапазон возраста: <b>{questionnaire.age_range}</b>\n\n" \
              f"🏳️ Национальность: <b>{questionnaire.nationality}</b>\n\n" \
              f"🎓 Образование: <b>{questionnaire.education}</b>\n\n" \
              f"🏙 Город, где получали образование: <b>{questionnaire.education_city}</b>\n\n" \
              f"🌆 Город текущего проживания: <b>{questionnaire.city}</b>\n\n" \
              f"🚗 Должен ли быть автомобиль: <b>{questionnaire.has_car}</b>\n\n" \
              f"🏡 Должно ли быть собственное жилье: <b>{questionnaire.has_own_housing}</b>\n\n" \
              f"💼 Чем должны заниматься: <b>{questionnaire.profession}</b>\n\n" \
              f"💍 Семейное положение: <b>{questionnaire.marital_status}</b>\n\n" \
              f"👶 Могут ли быть дети: <b>{questionnaire.has_children}</b>\n\n"
    return message


def check_name(name: str):
    response = {'name': None, 'message': None}
    if re.findall(r"\d+", name):
        response['message'] = "Имя не должно содержать цифры"
    else:
        response['name'] = name.capitalize()
    return response



