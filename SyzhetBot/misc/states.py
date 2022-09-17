from aiogram.dispatcher.filters.state import State, StatesGroup


class FeedBackState(StatesGroup):
    contact = State()
    addit_info = State()
