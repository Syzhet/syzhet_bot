from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


class AllMenuInlineKeyboard(InlineKeyboardMarkup):

    callback_menu = CallbackData('menu', 'type', 'name')

    def make_contact_callback(self, type, name):
        return self.callback_menu.new(type=type, name=name)

    def make_inline_keyboard(self, type, buttons, but_in_row=2):
        button_list = []
        for text, callback in buttons.items():
            button_list.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=self.make_contact_callback(type, callback),
                )
            )
            if len(button_list) == but_in_row:
                self.add(*button_list)
                button_list.clear()
        self.add(*button_list)
        return self
