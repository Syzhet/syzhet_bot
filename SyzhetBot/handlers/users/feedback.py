from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageNotModified

from emoji import emojize

from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard


FEEDBACK_BACK_MENU_KEYBOARD = AllMenuInlineKeyboard()
FEEDBACK_BACK_MENU_KEYBOARD.make_inline_keyboard(
    'feedback_menu',
    {
        emojize("Мобильный телефон :telephone_receiver:"): 'mobile',
        emojize("Telegram :airplane:"): 'telegram',
        emojize("Электронная почта :envelope:"): 'email',
        emojize('В меню :BACK_arrow:'): 'menu'
    },
    but_in_row=1
)


async def feedback(call: types.CallbackQuery):
    '''Обработка нажатия inline-кнопки "Обратная связь".'''
    with suppress(MessageNotModified):
        await call.message.edit_text(
            ('Выберите удобный для Вас способ связи. \n'
             'Выбор можно сделать нажатием на одну из кнопок ниже.'),
            reply_markup=FEEDBACK_BACK_MENU_KEYBOARD
        )


def register_feedback(dp: Dispatcher):
    '''Регистрация в диспетчере функции feedback.'''
    dp.register_callback_query_handler(
        feedback,
        AllMenuInlineKeyboard.callback_menu.filter(name='feedback')
    )
