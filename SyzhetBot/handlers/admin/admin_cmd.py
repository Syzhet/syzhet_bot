from typing import List, Union

from aiogram import Dispatcher, types
from aiohttp import ClientSession

from ...filters.admin import AdminFilter
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
        for resp in response:
            orders: Union[str, List] = []
            if resp['orders']:
                for ord in resp['orders']:
                    orders.append(
                        (f'id: {ord["id"]}\n'
                         f'Название: {ord["title"]}\n'
                         f'Описание: {ord["description"]}\n'
                         '-----------\n')
                    )
                orders = ''.join(orders)
            else:
                orders = 'Нет заказов'
            await message.answer(
                (f'id: {resp["id"]}\n'
                 f'usernmae: @{resp["username"]}\n'
                 f'telegram_id: {resp["telegram_id"]}\n'
                 f'updated: {resp["updated_on"]}\n'
                 f'orders: {orders}')
            )
    except KeyError:
        await message.answer(
            'Произошла ошибка. Попробуйте повторить запрос позже'
        )


def register_cmd(dp: Dispatcher):
    '''Регистрация в диспетчере функции cmd_users.'''

    dp.register_message_handler(
        cmd_users,
        AdminFilter(),
        commands=['users'],
        state='*'
    )
