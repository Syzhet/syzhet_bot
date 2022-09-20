from aiogram import Dispatcher, types
from aiogram.utils.markdown import hbold, hlink
from emoji import emojize

from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard

EXAMPLE_WORK_BACK_MENU_KEYBOARD = AllMenuInlineKeyboard()
EXAMPLE_WORK_BACK_MENU_KEYBOARD.make_inline_keyboard(
    'feedback_menu',
    {
        emojize('В меню :BACK_arrow:'): 'menu'
    }
)

BEHANCE = hlink('Behance', 'https://www.behance.net/khasguz')
DRIBBLE = hlink('Dribbble', 'https://dribbble.com/khasguz')


async def example_work(call: types.CallbackQuery):
    '''Обработка нажатия inline-кнопки "Примеры работ".'''
    await call.message.edit_text(
        (f'{emojize(":pushpin:")} Работы по направлению '
         f'{hbold("графического дизайна")} '
         f'вы можете посмотреть в моем профиле на <b>{BEHANCE}</b>.\n\n'
         f'{emojize(":pushpin:")} Если вас интересуют {hbold("иллюстрации")}, '
         f'то вам на мою страницу в <b>{DRIBBLE}</b>.'),
        reply_markup=EXAMPLE_WORK_BACK_MENU_KEYBOARD,
        disable_web_page_preview=True
    )


def register_example_work(dp: Dispatcher):
    '''Регистрация в диспетчере функции example_work в диспетчере.'''
    dp.register_callback_query_handler(
        example_work,
        AllMenuInlineKeyboard.callback_menu.filter(name='works')
    )
