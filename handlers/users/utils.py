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
