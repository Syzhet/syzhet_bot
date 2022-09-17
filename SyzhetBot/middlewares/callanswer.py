from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class CallAnswertMiddleware(BaseMiddleware):

    async def on_pre_process_callback_query(
        self, call: types.CallbackQuery,
        data: dict
    ):
        await call.answer()
