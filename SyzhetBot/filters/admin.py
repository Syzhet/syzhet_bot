from aiogram.dispatcher.filters import BoundFilter

from SyzhetBot.config import Config


class AdminFilter(BoundFilter):

    async def check(self, obj):
        """Проверка, что пользователь администартор."""

        config: Config = obj.bot.get('config')
        user_id = obj.from_user.id
        return user_id == config.tg_bot.admin_id
