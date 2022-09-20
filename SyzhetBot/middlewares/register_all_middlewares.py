from aiogram import Dispatcher

from .callanswer import CallAnswertMiddleware
from .environments import EnvironmentMiddleware
from .throttling import ThrottlingMiddleware


def register_all_middlewares(dp: Dispatcher, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(CallAnswertMiddleware())
