from pprint import pprint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

nationality_callback = CallbackData('chosen_nationality', 'nationality')
education_callback = CallbackData('chosen_education', 'education')
education_city_callback = CallbackData('chosen_education_city', 'education_city')
city_callback = CallbackData('user_city', 'city')
profession_callback = CallbackData('chosen_profession', 'profession')
marital_status_callback = CallbackData('chosen_marital_status', 'marital_status')
change_user_data_callback = CallbackData('chosen_item', 'item')
change_search_status_callback = CallbackData('chosen_status', 'status')
gender_callback = CallbackData('chosen_gender', 'gender')


def change_search_status_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Активный",
            callback_data=change_search_status_callback.new("active")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Неактивный",
            callback_data=change_search_status_callback.new("inactive")
        )
    )
    return markup


def get_callback_by_name(callback_name):
    callback_data = None
    if callback_name == 'education_city_callback':
        callback_data = education_city_callback
    elif callback_name == 'education_callback':
        callback_data = education_callback
    elif callback_name == 'city_callback':
        callback_data = city_callback
    elif callback_name == 'profession_callback':
        callback_data = profession_callback
    elif callback_name == 'marital_status_callback':
        callback_data = marital_status_callback
    elif callback_name == 'gender_callback':
        callback_data = gender_callback
    return callback_data


def universal_markup(data_list: list, callback_name, does_not_matter=False):
    markup = InlineKeyboardMarkup()
    callback = get_callback_by_name(callback_name)
    for item in enumerate(data_list):
        markup.add(
            InlineKeyboardButton(
                text=item[1],
                callback_data=callback.new(item[0])
            )
        )
    if does_not_matter:
        markup.add(
            InlineKeyboardButton(
                text="Не имеет значения",
                callback_data=callback.new(-1)
            )
        )
    return markup


def nationality_markup(nationalities):
    markup = InlineKeyboardMarkup(row_width=2)
    l = len(nationalities)
    x = 0
    if l % 2 != 0:
        while x < l - 1:
            markup.add(
                InlineKeyboardButton(
                    text=nationalities[x],
                    callback_data=nationality_callback.new(x)
                ),
                InlineKeyboardButton(
                    text=nationalities[x + 1],
                    callback_data=nationality_callback.new(x + 1)
                )
            )
            x += 2
        markup.add(
            InlineKeyboardButton(
                text=nationalities[x],
                callback_data=nationality_callback.new(x)
            )
        )
    else:
        while x < l:
            markup.add(
                InlineKeyboardButton(
                    text=nationalities[x],
                    callback_data=nationality_callback.new(x)
                ),
                InlineKeyboardButton(
                    text=nationalities[x + 1],
                    callback_data=nationality_callback.new(x + 1)
                )
            )
            x += 2
    return markup


def change_search_questionnaire_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Диапазон возраста',
            callback_data=change_user_data_callback.new('age_range')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Национальность',
            callback_data=change_user_data_callback.new('nationality')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Образование',
            callback_data=change_user_data_callback.new('education')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Город, где получал образование',
            callback_data=change_user_data_callback.new('education_city')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Город проживания',
            callback_data=change_user_data_callback.new('city')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Чем должен заниматься',
            callback_data=change_user_data_callback.new('profession')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Семейное положение',
            callback_data=change_user_data_callback.new('marital_status')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Должен ли быть автомобиль',
            callback_data=change_user_data_callback.new('has_car')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Должно ли быть собственное жилье',
            callback_data=change_user_data_callback.new('has_own_housing')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Могут ли быть дети',
            callback_data=change_user_data_callback.new('has_children')
        )
    )
    return markup


def change_user_data_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Имя',
            callback_data=change_user_data_callback.new('name')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Возраст',
            callback_data=change_user_data_callback.new('age')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Пол',
            callback_data=change_user_data_callback.new('gender')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Национальность',
            callback_data=change_user_data_callback.new('nationality')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Образование',
            callback_data=change_user_data_callback.new('education')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Город, где получали образование',
            callback_data=change_user_data_callback.new('education_city')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Город',
            callback_data=change_user_data_callback.new('city')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Чем занимаетесь',
            callback_data=change_user_data_callback.new('profession')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Семейное положение',
            callback_data=change_user_data_callback.new('marital_status')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Есть ли автомобиль',
            callback_data=change_user_data_callback.new('has_car')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Есть ли собственное жилье',
            callback_data=change_user_data_callback.new('has_own_housing')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text='Есть ли дети',
            callback_data=change_user_data_callback.new('has_children')
        )
    )
    return markup


# def get_marital_status_markup(statuses):
#     markup = InlineKeyboardMarkup(row_width=1)
#     for item in statuses:
#         markup.add(
#             InlineKeyboardButton(
#                 text=item,
#                 callback_data=marital_status_callback.new('123')
#             )
#         )
#     return markup


# def get_profession_markup(professions: list):
#     markup = InlineKeyboardMarkup(row_width=1)
#     for item in professions:
#         markup.add(
#             InlineKeyboardButton(
#                 text=item,
#                 callback_data=profession_callback.new('123')
#             )
#         )
#     return markup


# def city_markup(education_list: list):
#     markup = InlineKeyboardMarkup(row_width=1)
#     for item in education_list:
#         markup.add(
#             InlineKeyboardButton(
#                 text=item,
#                 callback_data=city_callback.new('123')
#             )
#         )
#     return markup


# def education_markup(education_list: list):
#     markup = InlineKeyboardMarkup(row_width=1)
#     for item in education_list:
#         markup.add(
#             InlineKeyboardButton(
#                 text=item,
#                 callback_data=education_callback.new('123')
#             )
#         )
#     return markup
