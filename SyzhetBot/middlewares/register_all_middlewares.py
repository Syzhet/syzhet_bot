from aiogram import Dispatcher

from .environments import EnvironmentMiddleware
from .throttling import ThrottlingMiddleware
from .callanswer import CallAnswertMiddleware


def register_all_middlewares(dp: Dispatcher, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(CallAnswertMiddleware())
