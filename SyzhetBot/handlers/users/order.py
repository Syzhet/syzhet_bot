import logging
from typing import Union

import aiohttp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from emoji import emojize

from SyzhetBot.config import Config
from SyzhetBot.handlers.users.contact_feedback import (email_contact_check,
                                                       mobile_contact_check)
from SyzhetBot.handlers.users.menu import menu
from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard
from SyzhetBot.misc.http_request import ApiHttpRequest
from SyzhetBot.misc.info_for_order import TYPE_WORKS
from SyzhetBot.misc.states import OrderState

ORDER_MENU_KEYBOARD = AllMenuInlineKeyboard()
ORDER_MENU_KEYBOARD.make_inline_keyboard(
    'category_order',
    {
        'Постер, баннер, афиша': 'poster',
        'Мерч': 'merch',
        'Логотип': 'logo',
        'Инфографика': 'infograph',
        'Лендинг': 'landing',
        'Иконки': 'icons',
        'Презентация': 'presentation',
        'Открытки': 'postcards',
        'Digital art': 'digital',
        'Иллюстрации по фото': 'photo_illustr',
        'Стикеры': 'stickers',
        'Другое': 'another',
        emojize('В меню :BACK_arrow:'): 'menu'
    }
)

CATEGORY_KEYBOARD = AllMenuInlineKeyboard()
CATEGORY_KEYBOARD.make_inline_keyboard(
    'category_description',
    {
        'Далее': 'further',
        'Отмена': 'cansel'
    },
    but_in_row=1
)

DESCRIPTION_CATEGORI_KEYBOARD = AllMenuInlineKeyboard()
DESCRIPTION_CATEGORI_KEYBOARD.make_inline_keyboard(
    'category_custom_info',
    {
        'Далее': 'further',
        'Отмена': 'cansel'
    },
    but_in_row=1
)

ORDER_CONTACT_KEYBOARD = AllMenuInlineKeyboard()
ORDER_CONTACT_KEYBOARD.make_inline_keyboard(
    'order_contact_menu',
    {
        emojize('Мобильный телефон :telephone_receiver:'): 'mobile',
        emojize('Telegram :airplane:'): 'telegram',
        emojize('Электронная почта :envelope:'): 'email',
        emojize('Отмена :cross_mark:'): 'cansel'
    },
    but_in_row=1
)

ORDER_CONTACT_CANSEL_KEYBOARD = AllMenuInlineKeyboard()
ORDER_CONTACT_CANSEL_KEYBOARD.make_inline_keyboard(
    'order_cansel_contact_menu',
    {
        emojize('Отмена :cross_mark:'): 'cansel'
    }
)

ORDER_URL = '/api/v1/orders/'


async def type_work(call: types.CallbackQuery, type_work):
    '''Подготовка описания и клавиатуры для конкретной категории заявки.'''
    text = TYPE_WORKS.get(type_work)
    await call.message.edit_text(
        text=text,
        reply_markup=CATEGORY_KEYBOARD
    )


async def order_menu(call: types.CallbackQuery, state: FSMContext):
    '''Обработка inline-кнопки "Оформить заявку".'''
    await call.message.edit_text(
        ('Выбирайте интересующий вас раздел. Я подробнее расскажу, '
         'что вы в итоге получите и сколько это будет стоить '
         f'{emojize(":right_arrow_curving_down:")}'),

        reply_markup=ORDER_MENU_KEYBOARD
    )
    await OrderState.menu.set()


async def choise_order_category(
    call: types.CallbackQuery,
    state: FSMContext,
    callback_data: dict
):
    '''Обработка нажатия на одну из inline-кнопок с названием категории.'''
    work = callback_data.get('name')
    async with state.proxy() as data:
        cat_work = data.get('cat_work')
        if cat_work:
            cat_work.append(work)
        else:
            data['cat_work'] = [work]
    await type_work(call, work)
    await OrderState.category.set()


async def cansel_order(
    call: types.CallbackQuery,
    state: FSMContext,
):
    '''Обработка нажатия inline-кнопки "Отмена" в ходе оформления заявки.'''
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await order_menu(call, state)


async def category_further_to_description(
    call: types.CallbackQuery,
):
    '''Обработка нажатия inline-кнопки "Далее" в меню описания категории.'''
    await call.message.edit_text(
        text=TYPE_WORKS.get('description'),
        reply_markup=DESCRIPTION_CATEGORI_KEYBOARD
    )
    await OrderState.description.set()


async def description_further_to_custom_info(
    call: types.CallbackQuery,
):
    '''Обработка нажатия inline-кнопки "Далее" в меню порядка работы.'''
    await call.message.edit_text(
            ('В свободном формате отправьте боту сообщение '
             'с дополнительной информацией.\n'
             'Например:\n'
             'Как к вам можно обращаться?\n'
             'Добавьте любые дополнительные пожелания.'),
        )
    await OrderState.custom_info.set()


async def order_get_contact(message: types.Message, state: FSMContext):
    '''Обработка сообщения введенного пользователем для доп. инф. по заявке.'''
    description = message.text
    async with state.proxy() as data:
        des_work = data.get('des_work')
        if des_work:
            des_work.append(description)
        else:
            data['des_work'] = [description]
    await message.answer(
        ('Выберите удобный для Вас способ связи. \n'
         'Выбор можно сделать нажатием на одну из кнопок ниже.'),
        reply_markup=ORDER_CONTACT_KEYBOARD
    )
    await OrderState.get_contact.set()


async def message_for_order_contact(call: types.CallbackQuery, type_contact):
    '''Отправка сообщения с предложением ввести контактную информацию.'''
    message_dict = {
        'mobile': ('Введите номер мобильного телефона \n'
                   'в формате +7XXXXXXXXXX'),
        'email':  ('Введите адрес электронной почты \n'
                   'в формате name@domen.ru'),
    }
    await call.message.edit_text(
        message_dict.get(type_contact),
        reply_markup=ORDER_CONTACT_CANSEL_KEYBOARD
    )


async def send_order_data(
    obj: Union[types.Message, types.CallbackQuery],
    state: FSMContext,
    config: Config,
    api_session: aiohttp.ClientSession,
    token: str
):
    '''Функция отправки сообщения владельцу бота со всеми данными по заявке.'''
    text_for_host = ('Контакт: {contact_text} '
                     'оставил заявку.\n'
                     'Категория заявки: {cat_data}\n'
                     'Описание заявки: {des_data}')
    answer_text = ('Спасибо за обращение!\n'
                   'Ваша заявака принята.\n'
                   'Я свяжусь с вами в ближайшее время.')
    order_data = await state.get_data()
    cat_data = ','.join(order_data.get('cat_work'))
    des_data = ','.join(order_data.get('des_work'))
    if isinstance(obj, types.CallbackQuery):
        contact_text = f'@{obj.from_user.username}'
        await obj.message.answer(answer_text)
        await menu(obj.message, state)
    else:
        contact_text = order_data.get('con_data')
        await obj.answer(answer_text)
        await menu(obj, state)
    await obj.bot.send_message(
        chat_id=config.tg_bot.host_id,
        text=text_for_host.format(
            contact_text=contact_text,
            cat_data=cat_data,
            des_data=des_data
        )
    )
    user_id = obj.from_user.id
    api_http_request = ApiHttpRequest(
        session=api_session,
        url=ORDER_URL
    )
    try:
        await api_http_request.create_order(
            token=token,
            title=cat_data,
            description=des_data,
            tg_id={'user_id': user_id}
        )
    except Exception as exp:
        logging.info(f'Ошибка при создании заказа - {exp}')


async def order_set_contact(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext,
    config: Config
):
    '''Обработка нажатия на одну из кнопок меню выбора способа связи.'''
    type_contact = callback_data.get('name')
    if type_contact == 'telegram':
        await send_order_data(call, state, config)
    else:
        await message_for_order_contact(call, type_contact)
        async with state.proxy() as data:
            data['type_contact'] = type_contact
        await OrderState.set_contact.set()


async def finish_order(
    message: types.Message,
    state: FSMContext,
    config: Config,
    api_session: aiohttp.ClientSession,
    token: str
):
    '''Обработка ввода контактной информации.'''
    async with state.proxy() as data:
        type_contact = data['type_contact']
        if type_contact == 'mobile':
            if not await mobile_contact_check(message):
                return
        elif type_contact == 'email':
            if not await email_contact_check(message):
                return
        await state.update_data(con_data=message.text)
        await send_order_data(
            message,
            state,
            config,
            api_session,
            token
        )


def register_order(dp: Dispatcher):
    '''
    Регистрация в диспетчере функций: order_menu,
    choise_order_category, category_further_to_description,
    cansel_order, description_further_to_custom_info,
    order_get_contact, order_set_contact, finish_order.
    '''
    dp.register_callback_query_handler(
        order_menu,
        AllMenuInlineKeyboard.callback_menu.filter(name='orders')
    )
    dp.register_callback_query_handler(
        choise_order_category,
        AllMenuInlineKeyboard.callback_menu.filter(type='category_order'),
        state=OrderState.menu
    )
    dp.register_callback_query_handler(
        category_further_to_description,
        AllMenuInlineKeyboard.callback_menu.filter(
            type='category_description',
            name='further'
        ),
        state=OrderState.category
    )
    dp.register_callback_query_handler(
        cansel_order,
        AllMenuInlineKeyboard.callback_menu.filter(name='cansel'),
        state=[
            OrderState.category,
            OrderState.description,
            OrderState.custom_info,
            OrderState.get_contact
        ]
    )
    dp.register_callback_query_handler(
        description_further_to_custom_info,
        AllMenuInlineKeyboard.callback_menu.filter(
            type='category_custom_info',
            name='further'
        ),
        state=OrderState.description
    )
    dp.register_message_handler(
        order_get_contact,
        state=OrderState.custom_info
    )
    dp.register_callback_query_handler(
        order_set_contact,
        AllMenuInlineKeyboard.callback_menu.filter(
            type='order_contact_menu'
        ),
        state=OrderState.get_contact
    )
    dp.register_message_handler(
        finish_order,
        state=OrderState.set_contact
    )
