from aiogram import Dispatcher

from .admin.admin_cmd import register_cmd
from .errors.errors_handler import register_errors_handler
from .users.contact_feedback import register_contact_feedback
from .users.echo import register_echo
from .users.example_work import register_example_work
from .users.feedback import register_feedback
from .users.help import register_help
from .users.menu import register_menu
from .users.order import register_order
from .users.start import register_start


def register_all_handlers(dp: Dispatcher):
    '''Регистрация всех хендлеров в диспетчере.'''
    register_errors_handler(dp)
    register_start(dp)
    register_menu(dp)
    register_help(dp)
    register_example_work(dp)
    register_feedback(dp)
    register_contact_feedback(dp)
    register_order(dp)
    register_echo(dp)
    register_cmd(dp)
