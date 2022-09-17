from typing import Union

from aiogram import types, Dispatcher
from emoji import emojize

from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard


MAIN_MENU_KEYBOARD = AllMenuInlineKeyboard(row_width=2)
MAIN_MENU_KEYBOARD.make_inline_keyboard(
    'main_menu',
    {
        'Примеры работ': 'works',
        'Оформить заявку': 'orders',
        'Обратная связь': 'feedback',
    }
)


async def menu(obj: Union[types.Message, types.CallbackQuery]):
    text_emoji = emojize(":black_medium-small_square:")
    text = ('Здесь вы можете:\n'
            f'{text_emoji} посмотреть мое портфолио;\n'
            f'{text_emoji} заказать у меня работу;\n'
            f'{text_emoji} запросить обратную связь.')
    if isinstance(obj, types.Message):
        await obj.answer(text=text, reply_markup=MAIN_MENU_KEYBOARD)
    else:
        await obj.message.edit_text(text=text, reply_markup=MAIN_MENU_KEYBOARD)


def register_menu(dp: Dispatcher):
    dp.register_message_handler(
        menu,
        commands=['menu']
    )
    dp.register_callback_query_handler(
        menu,
        AllMenuInlineKeyboard.callback_menu.filter(name='menu')
    )
