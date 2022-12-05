from aiogram import Dispatcher

from ..config import Config
from .api_session import ApiMiddlware
from .callanswer import CallAnswertMiddleware
from .environments import EnvironmentMiddleware
from .throttling import ThrottlingMiddleware


def register_all_middlewares(
    dp: Dispatcher,
    config: Config,
):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(CallAnswertMiddleware())
    dp.setup_middleware(ApiMiddlware(config.misc))
