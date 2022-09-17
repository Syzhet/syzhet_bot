from aiogram import types, Dispatcher


async def echo(message: types.Message):
    await message.reply('Такая команда не зарегистрирована')


def register_echo(dp: Dispatcher):
    dp.register_message_handler(
        echo,
        state='*',
        content_types=types.ContentType.ANY
    )