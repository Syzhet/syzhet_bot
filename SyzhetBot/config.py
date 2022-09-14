from os import getenv

from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class DbConfig:
    host: str
    database: str
    user: str
    password: str


@dataclass
class Miscellaneous:
    others_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config():
    load_dotenv()
    return Config(
        tg_bot=TgBot(
            token=getenv('BOT_TOKEN'),
            admin_id=int(getenv('ADMIN')),
            use_redis=False
        ),
        db=DbConfig(
            host=getenv('HOST'),
            database=getenv('DATABASE'),
            user=getenv('USER'),
            password=getenv('PASSWORD')
        ),
        misc=Miscellaneous()
    )