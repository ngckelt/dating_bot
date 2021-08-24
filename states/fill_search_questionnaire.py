from aiogram.dispatcher.filters.state import StatesGroup, State


class FillSearchQuestionnaire(StatesGroup):
    get_min_age = State()
    get_max_age = State()
    get_nationality = State()
    get_nationality_by_message = State()
    get_education = State()
    get_education_city = State()
    get_education_city_candidate = State()
    get_education_city_by_message = State()
    get_city = State()
    get_city_by_message = State()
    get_city_candidate = State()
    get_profession = State()
    get_marital_status = State()
    has_car = State()
    has_own_housing = State()
    has_children = State()
