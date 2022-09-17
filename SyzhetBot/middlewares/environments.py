from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def pre_process(self, update: types.Update, data: dict):
        data.update(self.kwargs)