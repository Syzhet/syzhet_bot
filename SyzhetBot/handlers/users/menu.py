from typing import Union

from aiogram import types, Dispatcher

from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard


async def menu(obj: Union[types.Message, types.CallbackQuery]):
    main_menu_keyboard = AllMenuInlineKeyboard(row_width=2)
    main_menu_keyboard.make_inline_keyboard(
        'main_menu',
        {
            'Примеры работ': 'works',
            'Оформить заявку': 'orders',
            'Обратная связь': 'feedback',
        }
    )
    text = ('Здесь вы можете:\n'
            '&#9726 посмотреть мое портфолио;\n'
            '&#9726 заказать у меня работу;\n'
            '&#9726 запросить обратную связь.')
    if isinstance(obj, types.Message):
        await obj.answer(text=text, reply_markup=main_menu_keyboard)
    else:
        await obj.message.edit_text(text=text, reply_markup=main_menu_keyboard)


def register_menu(dp: Dispatcher):
    dp.register_message_handler(
        menu,
        commands=['menu']
    )
    dp.register_callback_query_handler(
        menu,
        AllMenuInlineKeyboard.callback_menu.filter(name='menu')
    )
