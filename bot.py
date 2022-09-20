import asyncio
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from SyzhetBot.config import load_config
from SyzhetBot.middlewares.register_all_middlewares import (
    register_all_middlewares
)
from SyzhetBot.filters.register_all_filters import register_all_filters
from SyzhetBot.handlers.register_all_handlers import register_all_handlers

from SyzhetBot.services.set_bot_commands import set_defaults_commands


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            u'%(filename)s:%(lineno)d: '
            u'#%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
        )
    )
    '''Основная функция запуска бота.'''
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
