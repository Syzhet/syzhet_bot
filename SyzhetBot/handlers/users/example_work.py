from aiogram import types, Dispatcher
from aiogram.utils.markdown import hbold, hlink
from emoji import emojize

from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard


async def example_work(call: types.CallbackQuery):
    feedback_back_menu_keyboard = AllMenuInlineKeyboard()
    feedback_back_menu_keyboard.make_inline_keyboard(
        'feedback_menu',
        {
            emojize('В меню :BACK_arrow:'): 'menu'
        }
    )
    behance = hlink('Behance', 'https://www.behance.net/khasguz')
    dribble = hlink('Dribbble', 'https://dribbble.com/khasguz')
    await call.message.edit_text(
        (f'{emojize(":pushpin:")} Работы по направлению '
         f'{hbold("графического дизайна")} '
         f'вы можете посмотреть в моем профиле на <b>{behance}</b>.\n\n'
         f'{emojize(":pushpin:")} Если вас интересуют {hbold("иллюстрации")}, '
         f'то вам на мою страницу в <b>{dribble}</b>.'),
        reply_markup=feedback_back_menu_keyboard,
        disable_web_page_preview=True
    )


def register_example_work(dp: Dispatcher):
    dp.register_callback_query_handler(
        example_work,
        AllMenuInlineKeyboard.callback_menu.filter(name='works')
    )
