from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from emoji import emojize

from SyzhetBot.misc.info_for_order import TYPE_WORKS
from SyzhetBot.keyboards.inline import AllMenuInlineKeyboard
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
        emojize("Мобильный телефон :telephone_receiver:"): 'mobile',
        emojize("Telegram :airplane:"): 'telegram',
        emojize("Электронная почта :envelope:"): 'email',
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
             'Например:'
             'Как к вам можно обращаться?\n'
             'Добавьте любые дополнительные пожелания.'),
        )
    await OrderState.custom_info.set()


async def order_get_contact(message: types.Message, state: FSMContext):
    '''Обработка сообщения введенного пользователем для доп. инф. по заявке'''
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





def register_order(dp: Dispatcher):
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
            OrderState.custom_info
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
