from aiogram import Dispatcher

from .users.start import register_start
from .users.menu import register_menu
from .users.help import register_help
from .users.example_work import register_example_work
from .users.echo import register_echo
from .users.feedback import register_feedback


def register_all_handlers(dp: Dispatcher):
    register_start(dp)
    register_menu(dp)
    register_help(dp)
    register_example_work(dp)
    register_feedback(dp)
    register_echo(dp)
