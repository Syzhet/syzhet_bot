from aiogram import Dispatcher
from aiohttp import ClientSession

from .callanswer import CallAnswertMiddleware
from .environments import EnvironmentMiddleware
from .throttling import ThrottlingMiddleware
from .api_session import ApiMiddlware
from ..config import Config


def register_all_middlewares(
    dp: Dispatcher,
    config: Config,
    session: ClientSession
):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(CallAnswertMiddleware())
    dp.setup_middleware(ApiMiddlware(session, config.misc))
