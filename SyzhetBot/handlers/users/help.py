from aiogram import types, Dispatcher


async def cmd_help(message: types.Message):
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
        commands=['help']
    )
