from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeSearchQuestionnaire(StatesGroup):
    chose_item = State()
    change_item = State()
    change_min_age = State()
    change_max_age = State()
    change_nationality = State()
    change_nationality_by_message = State()
    change_education = State()
    change_education_city = State()
    change_education_city_by_message = State()
    change_education_city_candidate = State()
    change_city = State()
    change_city_by_message = State()
    change_city_candidate = State()
    change_profession = State()
    change_marital_status = State()
    change_has_car = State()
    change_has_own_housing = State()
    change_has_children = State()


