from pprint import pprint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

nationality_callback = CallbackData('chosen_nationality', 'nationality')
education_callback = CallbackData('chosen_education', 'education')
education_city_callback = CallbackData('chosen_education_city', 'education_city')
city_callback = CallbackData('user_city', 'city')
profession_callback = CallbackData('chosen_profession', 'profession')
marital_status_callback = CallbackData('chosen_marital_status', 'marital_status')


def universal_markup(data_list: list, callback_name):
    markup = InlineKeyboardMarkup()
    callback_data = None
    for item in enumerate(data_list):
        if callback_name == 'education_city_callback':
            callback_data = education_city_callback.new(item[0])
        elif callback_name == 'education_callback':
            callback_data = education_callback.new(item[0])
        elif callback_name == 'city_callback':
            callback_data = city_callback.new(item[0])
        elif callback_name == 'profession_callback':
            callback_data = profession_callback.new(item[0])
        elif callback_name == 'marital_status_callback':
            callback_data = marital_status_callback.new(item[0])
        markup.add(
            InlineKeyboardButton(
                text=item[1],
                callback_data=callback_data
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
