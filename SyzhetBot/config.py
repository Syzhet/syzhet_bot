from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class TgBot:
    token: str
    admin_id: int
    host_id: int
    use_redis: bool


@dataclass
class DbConfig:
    host: str
    database: str
    user: str
    password: str


@dataclass
class Miscellaneous:
    api_url: str
    api_username: str
    api_password: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config():
    '''Установка основных параметров для работы бота.'''
    load_dotenv()
    return Config(
        tg_bot=TgBot(
            token=getenv('BOT_TOKEN'),
            admin_id=int(getenv('ADMIN_ID')),
            host_id=int(getenv('HOST_ID')),
            use_redis=False if getenv('USE_REDIS') == 'False' else True
        ),
        db=DbConfig(
            host=getenv('HOST_DB'),
            database=getenv('DATABASE'),
            user=getenv('USER_DB'),
            password=getenv('PASSWORD_DB')
        ),
        misc=Miscellaneous(
            api_url=getenv('API_URL'),
            api_username=getenv('API_USERNAME'),
            api_password=getenv('API_PASSWORD')
        )
    )
