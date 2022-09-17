from aiogram import types


async def set_defaults_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('menu', 'Вызов главного меню')
    ])
