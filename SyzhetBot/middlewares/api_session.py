import aiohttp
from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from ..misc.http_request import ApiHttpRequest


class ApiMiddlware(LifetimeControllerMiddleware):
    def __init__(self, misc):
        super().__init__()
        self.api_url = misc.api_url
        self.api_username = misc.api_username
        self.api_password = misc.api_password

    def create_session(self):
        return aiohttp.ClientSession(self.api_url)

    async def pre_process(self, update: types.Update, data: dict, *args):
        session = self.create_session()
        data['api_session'] = session
        api_http_request = ApiHttpRequest(
            session=session,
            url='/api/v1/token/'
            )
        token = await api_http_request.get_token(
            username=self.api_username,
            password=self.api_password
        )
        data['token'] = token

    async def post_process(self, update: types.Update, data: dict, *args):
        await data['api_session'].close()
        del data['token']
