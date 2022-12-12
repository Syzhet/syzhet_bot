from aiogram import Dispatcher, types
from aiohttp import ClientSession

from ...filters.admin import AdminFilter
from ...misc.for_admin_commands import (list_order_to_message,
                                        list_user_to_message,
                                        order_obj_to_message,
                                        user_obj_to_message)
from ...misc.http_request import ApiHttpRequest

USER_URL = '/api/v1/users/'
ORDER_URL = '/api/v1/orders/'


async def cmd_users(
    message: types.Message,
    api_session: ClientSession,
    token: str
):
    '''Обработка команды /users.'''

    params = message.get_args().split()
    if params:
        if len(params) == 2:
            params = {params[0]: params[1]}
    api_http_request = ApiHttpRequest(api_session, USER_URL)
    response = await api_http_request.get_users(token, params)
    try:
        await list_user_to_message(message, response)
    except KeyError:
        await message.answer(
            'Произошла ошибка. Попробуйте изменить запрос'
        )


async def cmd_orders(
    message: types.Message,
    api_session: ClientSession,
    token: str
):
    '''Обработка команды /orders.'''

    params = message.get_args().split()
    if params:
        if len(params) == 2:
            params = {params[0]: params[1]}
    api_http_request = ApiHttpRequest(api_session, ORDER_URL)
    response = await api_http_request.get_orders(token, params)
    try:
        await list_order_to_message(message, response)
    except KeyError:
        await message.answer(
            'Произошла ошибка. Попробуйте изменить запрос'
        )


async def cmd_user_id(
    message: types.Message,
    api_session: ClientSession,
    token: str
):
    """Обработка команды /user id."""

    try:
        id = int(message.get_args())
    except ValueError:
        await message.answer(
            'Произошла ошибка. ID должен быть целым числом!'
        )
    api_http_request = ApiHttpRequest(api_session, USER_URL)
    response = await api_http_request.get_user_from_id(token, id)
    try:
        await user_obj_to_message(message, response)
    except KeyError:
        await message.answer(
            'Произошла ошибка. Попробуйте изменить запрос'
        )


async def cmd_order_id(
    message: types.Message,
    api_session: ClientSession,
    token: str
):
    """Обработка команды /order id."""

    try:
        id = int(message.get_args())
    except ValueError:
        await message.answer(
            'Произошла ошибка. ID должен быть целым числом!'
        )
    api_http_request = ApiHttpRequest(api_session, ORDER_URL)
    response = await api_http_request.get_order_from_id(token, id)
    try:
        await order_obj_to_message(message, response)
    except KeyError:
        await message.answer(
            'Произошла ошибка. Попробуйте изменить запрос'
        )


async def cmd_users_count(
    message: types.Message,
    api_session: ClientSession,
    token: str
):
    '''Обработка команды /ucount.'''

    api_http_request = ApiHttpRequest(api_session, USER_URL)
    response = await api_http_request.get_user_count(token)
    count = response.get('count_users').split()[-1]
    return await message.answer(
        f'Количество зарегистрированных пользователей: {count}'
    )


def register_cmd(dp: Dispatcher):
    '''Регистрация в диспетчере функции cmd_users.'''

    dp.register_message_handler(
        cmd_users,
        AdminFilter(),
        commands=['users'],
        state='*'
    )
    dp.register_message_handler(
        cmd_orders,
        AdminFilter(),
        commands=['orders'],
        state='*'
    )
    dp.register_message_handler(
        cmd_user_id,
        AdminFilter(),
        commands=['user'],
        state='*'
    )
    dp.register_message_handler(
        cmd_order_id,
        AdminFilter(),
        commands=['order'],
        state='*'
    )
    dp.register_message_handler(
        cmd_users_count,
        AdminFilter(),
        commands=['ucount'],
        state='*'
    )
