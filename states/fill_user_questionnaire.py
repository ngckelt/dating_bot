from aiogram.dispatcher.filters.state import StatesGroup, State


class FillUserQuestionnaire(StatesGroup):
    get_name = State()
    get_age = State()
    get_nationality = State()
    get_education = State()
    get_education_city = State()
    get_city = State()
    get_profession = State()
    get_marital_status = State()
    has_car = State()
    has_own_housing = State()
    has_children = State()
