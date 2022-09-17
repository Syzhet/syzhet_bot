import asyncio
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from SyzhetBot.config import load_config
from SyzhetBot.filters.admin import AdminFilter
from SyzhetBot.handlers.users.start import register_start
from SyzhetBot.handlers.users.menu import register_menu
from SyzhetBot.handlers.users.help import register_help
from SyzhetBot.handlers.users.echo import register_echo
from SyzhetBot.middlewares.environments import EnvironmentMiddleware
from SyzhetBot.middlewares.throttling import ThrottlingMiddleware
from SyzhetBot.services.set_bot_commands import set_defaults_commands


logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config)) # передаем нужные middleware
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter) #передаем нужные фильтры


def register_all_handlers(dp):
    # register_admin(dp) - регистрация handlers
    register_start(dp)
    register_menu(dp)
    register_help(dp)
    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d: #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_defaults_commands(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
