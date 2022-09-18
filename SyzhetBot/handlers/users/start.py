from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from .menu import menu


async def cmd_start(message: types.Message, state: FSMContext):
    '''Обработка команды /start.'''
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await message.answer(
        (f'Приветствую Вас, {message.from_user.full_name} &#128075\n'
         'С вами на связи Гузель и мой бот-помощник.\n'
         'Я являюсь графическим дизайнером и иллюстратором.\n'),
    )
    await menu(message, state)


def register_start(dp: Dispatcher):
    dp.register_message_handler(
        cmd_start,
        commands=['start'],
        state='*'
    )