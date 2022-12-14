from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiohttp import ClientSession

from SyzhetBot.misc.throttling import rate_limit

from ...misc.http_request import ApiHttpRequest
from .menu import menu

CREATE_USER_URL = '/api/v1/users/'


@rate_limit(limit=3)
async def cmd_start(
    message: types.Message,
    state: FSMContext,
    api_session: ClientSession,
    token: str
):
    """Обработка команды /start."""

    current_state = await state.get_state()
    if current_state:
        await state.finish()
    await message.answer(
        (f'Приветствую Вас, {message.from_user.full_name} &#128075\n'
         'С вами на связи Гузель и мой бот-помощник.\n'
         'Я являюсь графическим дизайнером и иллюстратором.\n'),
    )
    await menu(message, state)
    telegram_id = message.from_user.id
    username = message.from_user.username
    api_http_request = ApiHttpRequest(api_session, CREATE_USER_URL)
    await api_http_request.get_or_create_user(token, username, telegram_id)


def register_start(dp: Dispatcher):
    '''Регистрация в диспетчере функции cmd_start.'''
    dp.register_message_handler(
        cmd_start,
        commands=['start'],
        state='*'
    )
