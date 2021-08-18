def prepare_answers(answers):
    answers = answers.split('\n')
    return answers


def translate_choice(choice):
    return {
        "yes": "Да",
        "no": "Нет",
        "does_not_matter": "Не имеет значения"
    }.get(choice)


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
    message = f"Ваши данные:\n" \
              f"Имя: {user.name}\n" \
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
    return message


def create_message_by_search_questionnaire(questionnaire):
    message = f"Ваша анкета для поиска:\n" \
              f"Диапазон возраста: {questionnaire.age_range}\n" \
              f"Национальность: {questionnaire.nationality}\n" \
              f"Образование: {questionnaire.education}\n" \
              f"Город, где получали образование: {questionnaire.education_city}\n" \
              f"Город текущего проживания: {questionnaire.city}\n" \
              f"Должен ли быть автомобиль: {questionnaire.has_car}\n" \
              f"Должно ли быть собственное жилье: {questionnaire.has_own_housing}\n" \
              f"Чем должны заниматься: {questionnaire.profession}\n" \
              f"Семейное положение: {questionnaire.marital_status}\n" \
              f"Могут ли быть дети: {questionnaire.has_children}\n"
    return message





