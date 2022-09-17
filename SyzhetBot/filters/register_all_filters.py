from aiogram import Dispatcher

from .admin import AdminFilter


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
