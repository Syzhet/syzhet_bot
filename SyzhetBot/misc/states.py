from aiogram.dispatcher.filters.state import State, StatesGroup


class FeedBackState(StatesGroup):
    contact = State()
    addit_info = State()


class OrderState(StatesGroup):
    menu = State()
    category = State()
    description = State()
    custom_info = State()
    get_contact = State()
    set_contact = State()
