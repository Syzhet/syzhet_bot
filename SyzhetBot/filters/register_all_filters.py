from aiogram import Dispatcher

from .admin import AdminFilter


def register_all_filters(dp: Dispatcher):
    '''Регистрация всех фильтров в диспетчере.'''
    dp.filters_factory.bind(AdminFilter)
