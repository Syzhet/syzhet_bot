from typing import Dict, List, Optional

import aiohttp


class ApiHttpRequest:
    """Класс для работы с запросами к API."""

    def __init__(self, session: aiohttp.ClientSession, url: str):
        self.session = session
        self.url = url

    async def get_token(self, username: str, password: str) -> str:
        """Возвращает токен для доступа к эндпоинтам API."""

        async with self.session.post(
            url=self.url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'username': username, 'password': password}
        ) as resp:
            return await resp.json()

    async def get_obj_list(
        self,
        token: str,
        params: Optional[Dict[str, str]] = None
    ) -> List[Optional[Dict[str, str]]]:
        """Возвращает список данных, полученных через API."""

        async with self.session.get(
            url=self.url,
            headers={'Authorization': f'Bearer {token}'},
            params=params
        ) as resp:
            return await resp.json()

    async def get_obj_from_id(
        self,
        token: str,
        id: int
    ):
        """Возвращает единичный объект данных, полученных через API."""

        url = '{0}{1}/'.format(self.url, id)
        async with self.session.get(
            url=url,
            headers={'Authorization': f'Bearer {token}'}
        ) as resp:
            return await resp.json()

    async def get_obj_count(
        self,
        token: str,
    ):
        """Возвращает количество объектов в выбранной таблице базы данных."""

        url = '{0}count/'.format(self.url)
        async with self.session.get(
            url=url,
            headers={'Authorization': f'Bearer {token}'}
        ) as resp:
            return await resp.json()

    async def get_users(
        self,
        token: str,
        params: Optional[Dict[str, str]] = None
    ) -> List[Optional[Dict[str, str]]]:
        """Возвращает список пользователей, полученных через API."""

        return await self.get_obj_list(token, params)

    async def get_or_create_user(
        self,
        token: str,
        username: str,
        telegram_id: str
    ):
        """Возвращает пользователя, либо создает нового в базе данных."""

        params = {'tgid': telegram_id}
        user = await self.get_users(token, params)
        if not user:
            async with self.session.post(
                url=self.url,
                headers={'Authorization': f'Bearer {token}'},
                json={'username': username, 'telegram_id': telegram_id}
            ) as resp:
                return await resp.json()
        return user

    async def get_user_id(
        self,
        token: str,
        tg_id: Dict[str, int]
    ) -> int:
        """Функция получения пользователя по id."""

        user = await self.get_users(
            token=token,
            params=tg_id
        )
        try:
            return user[0]['id']
        except (IndexError, KeyError):
            return 'Error. This user not found'

    async def create_order(
        self,
        token: str,
        title: str,
        description: str,
        user_id: Dict[str, int]
    ):
        """Функция создания заказа."""

        async with self.session.post(
            url=self.url,
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': title,
                'description': description,
                'user_id': int(user_id)
            }
        ) as resp:
            return await resp.json()

    async def get_orders(
        self,
        token: str,
        params: Optional[Dict[str, str]] = None
    ) -> List[Optional[Dict[str, str]]]:
        """Возвращает список заказов, полученных через API."""

        return await self.get_obj_list(token, params)

    async def get_user_from_id(
        self,
        token: str,
        id: int
    ):
        """Получение пользователя по id."""

        return await self.get_obj_from_id(token, id)

    async def get_order_from_id(
        self,
        token: str,
        id: int
    ):
        """Получение заказа по id."""

        return await self.get_obj_from_id(token, id)

    async def get_user_count(
        self,
        token: str
    ):
        """Возвращает количество пользователей в базе данных."""

        return await self.get_obj_count(token)

    async def get_order_count(
        self,
        token: str
    ):
        """Возвращает количество заказов в базе данных."""

        return await self.get_obj_count(token)
