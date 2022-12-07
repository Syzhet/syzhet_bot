from typing import Dict, List, Optional

import aiohttp


class ApiHttpRequest:
    def __init__(self, session: aiohttp.ClientSession, url: str):
        self.session = session
        self.url = url

    async def get_token(self, username: str, password: str) -> str:
        async with self.session.post(
            url=self.url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'username': username, 'password': password}
        ) as resp:
            return await resp.json()

    async def create_user(
        self,
        token: str,
        username: str,
        telegram_id: str
    ):
        async with self.session.post(
            url=self.url,
            headers={'Authorization': f'Bearer {token}'},
            json={'username': username, 'telegram_id': telegram_id}
        ) as resp:
            return await resp.json()

    async def get_users(
        self,
        token,
        params=None
    ) -> List[Optional[Dict[str, str]]]:
        """Возвращает список пользователей, полученных через API."""

        async with self.session.get(
            url=self.url,
            headers={'Authorization': f'Bearer {token}'},
            params=params
        ) as resp:
            return await resp.json()
