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
