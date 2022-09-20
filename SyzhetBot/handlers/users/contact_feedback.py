import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from emoji import emojize

from SyzhetBot.config import Config
from SyzhetBot.handlers.users.feedback import feedback
from SyzhetBot.handlers.users.menu import menu
from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard
from SyzhetBot.misc.states import FeedBackState

CANSEL_CONTACT_KEYBOARD = AllMenuInlineKeyboard()
CANSEL_CONTACT_KEYBOARD.make_inline_keyboard(
    'contact_menu',
    {emojize('Отмена :cross_mark:'): 'cansel'}
)


async def message_for_contact(call: types.CallbackQuery, type_contact):
    '''Отправка сообщения с предложением ввести контактную информацию.'''
    message_dict = {
        'mobile': ('Введите номер мобильного телефона \n'
                   'в формате +7XXXXXXXXXX'),
        'email':  ('Введите адрес электронной почты \n'
                   'в формате name@domen.ru'),
    }
    await call.message.edit_text(
        message_dict.get(type_contact),
        reply_markup=CANSEL_CONTACT_KEYBOARD
    )


async def mobile_contact_check(message: types.Message):
    '''Проверка правильности ввода номера телефона.'''
    if len(message.text) != 12:
        await message.answer('Номер должен состоять из 12 символов')
        return
    elif not message.text[1:].isdigit():
        await message.answer(
            'Номер должен содержать только код "+7" и 10 цифр'
        )
        return
    elif not message.text.startswith('+7'):
        await message.answer(
            'Необходимо указать код +7 в начале номера'
        )
        return
    return True


async def email_contact_check(message: types.Message):
    '''Проверка правильности ввода email.'''
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    )
    email = message.text
    if not re.fullmatch(regex, email):
        await message.answer(
            'Введите кореектный email'
        )
        return
    return True


async def contact_feedback(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext,
    config: Config
):
    '''Обработка нажатия на одну из кнопок меню выбора способа связи.'''
    type_contact = callback_data.get('name')
    if type_contact == 'telegram':
        await call.message.edit_text(
            ('Спасибо за обращение! \nЯ свяжусь с вами в ближайшее время.')
        )
        await menu(call.message)

        text = (f'Контакт: @{call.from_user.username} просит связаться с ним.')
        await call.bot.send_message(
            chat_id=config.tg_bot.host_id,
            text=text
        )
    else:
        async with state.proxy() as data:
            data['type_contact'] = type_contact
        await message_for_contact(call, type_contact)
        await FeedBackState.contact.set()


async def cansel_contact_feedback(
    call: types.CallbackQuery,
    state: FSMContext
):
    '''Обработка нажатия inline-кнопки "Отмена".'''
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await feedback(call)


async def additional_info_contact(message: types.Message, state: FSMContext):
    '''Обработка ввода контактной информации.'''
    async with state.proxy() as data:
        type_contact = data['type_contact']
        if type_contact == 'mobile':
            if not await mobile_contact_check(message):
                return
        elif type_contact == 'email':
            if not await email_contact_check(message):
                return
        await state.update_data(contact=message.text)
        await message.answer(
            ('В свободном формате укажите как к вам можно обращаться, '
             'удобное время для звонка '
             'и дополнительные пожелания.'),
            reply_markup=CANSEL_CONTACT_KEYBOARD
        )
        await FeedBackState.addit_info.set()


async def send_contact_info_to_host(
    message: types.Message,
    state: FSMContext,
    config: Config
):
    '''Обработка ввода доп. информации и отправка контакта владельцу бота.'''
    await message.answer(
        ('Спасибо за обращение! \nЯ свяжусь с вами в ближайшее время.')
    )
    await state.update_data(adit_info=message.text)
    contact_data = await state.get_data()
    text = (f'Контакт: {contact_data.get("contact")} просит связаться с ним.\n'
            f'Дополнительная информация: {contact_data.get("adit_info")}')
    await message.bot.send_message(
        chat_id=config.tg_bot.host_id,
        text=text
    )
    await state.finish()
    await menu(message)


def register_contact_feedback(dp: Dispatcher):
    '''
    Регистрация в диспетчере функций: contact_feedback,
    cansel_contact_feedback, additional_info_contact,
    send_contact_info_to_host.
    '''
    dp.register_callback_query_handler(
        contact_feedback,
        AllMenuInlineKeyboard.callback_menu.filter(type='feedback_menu')
    )
    dp.register_callback_query_handler(
        cansel_contact_feedback,
        AllMenuInlineKeyboard.callback_menu.filter(
            type='contact_menu',
            name='cansel'
        ),
        state=[FeedBackState.contact, FeedBackState.addit_info]
    )
    dp.register_message_handler(
        additional_info_contact,
        state=FeedBackState.contact
    )
    dp.register_message_handler(
        send_contact_info_to_host,
        state=FeedBackState.addit_info
    )
