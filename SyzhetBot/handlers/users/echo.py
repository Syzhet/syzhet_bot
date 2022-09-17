from aiogram import types, Dispatcher

from .help import cmd_help


ID_STICKER = ('CAACAgIAAxkBAAEFzJljHY8rk_'
              '-my6RYgA1vva00U8d2-wACnRYAAkqDaUtBibBPJTndlykE')


async def echo(message: types.Message):
    await message.reply('Я не знаю такой команды...')
    await message.bot.send_sticker(message.from_user.id, ID_STICKER)
    await cmd_help(message)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(
        echo,
        state='*',
        content_types=types.ContentType.ANY
    )
