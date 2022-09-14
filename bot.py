import asyncio
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from SyzhetBot.config import load_config
from SyzhetBot.filters.admin import AdminFilter
from SyzhetBot.handlers.admin import register_admin
from SyzhetBot.handlers.echo import register_echo


logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher):
    # dp.setup_middleware() # передаем нужные middleware
    pass


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter) #передаем нужные фильтры


def register_all_handlers(dp):
    # register_admin(dp) - регистрация handlers
    register_admin(dp)
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

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

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