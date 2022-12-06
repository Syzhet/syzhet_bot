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
    '''Обработка сообщения users.'''
    params = message.get_args().split()
    if params:
        if len(params) == 2:
            params = {params[0]: params[1]}
    api_http_request = ApiHttpRequest(api_session, USER_URL)
    response = await api_http_request.get_users(token, params)
    await message.answer(
        f'{response}'
    )


def register_cmd(dp: Dispatcher):
    '''Регистрация в диспетчере функции cmd_users.'''
    dp.register_message_handler(
        cmd_users,
        AdminFilter(),
        commands=['users'],
        state='*'
    )
