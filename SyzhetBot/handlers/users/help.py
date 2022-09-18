from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def cmd_help(message: types.Message, state: FSMContext):
    '''Обработка команды /help.'''
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await message.answer(
        (f'{message.from_user.full_name}, '
         'для начала работы с ботом необходимо, '
         'выполнить одну из следуюших команд:\n'
         '/start - запустить бота\n'
         '/menu - вызов главного меню')
    )


def register_help(dp: Dispatcher):
    dp.register_message_handler(
        cmd_help,
        commands=['help'],
        state='*'
    )
