from aiogram import types, Dispatcher
from .menu import menu


async def cmd_start(message: types.Message):
    await message.answer(
        (f'Приветствую Вас, {message.from_user.full_name} &#128075\n'
         'С вами на связи Гузель и мой бот-помощник.\n'
         'Я являюсь графическим дизайнером и иллюстратором.\n'),
    )
    await menu(message)


def register_start(dp: Dispatcher):
    dp.register_message_handler(
        cmd_start,
        commands=['start']
    )
