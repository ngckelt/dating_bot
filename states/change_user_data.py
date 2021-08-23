from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeUserData(StatesGroup):
    chose_item = State()
    change_item = State()
    change_name = State()
    change_gender = State()
    change_age = State()
    change_nationality = State()
    change_education = State()
    change_education_city = State()
    change_city = State()
    change_profession = State()
    change_marital_status = State()
    change_has_car = State()
    change_has_own_housing = State()
    change_has_children = State()


