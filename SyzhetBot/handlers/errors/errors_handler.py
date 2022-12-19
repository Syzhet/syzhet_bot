import logging

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import (BadRequest, BotBlocked, BotKicked,
                                      CantGetUpdates, CantParseEntities,
                                      MessageCantBeDeleted,
                                      MessageCantBeEdited,
                                      MessageCantBeForwarded,
                                      MessageNotModified, MessageTextIsEmpty,
                                      MessageToDeleteNotFound,
                                      MessageToEditNotFound,
                                      MessageToForwardNotFound,
                                      TelegramAPIError)


async def errors_handler(update: types.Update, exception):
    """Функция обработки исключений в работе бота."""

    if isinstance(exception, MessageCantBeDeleted):
        logging.info('message can\'t be deleted')
        return True

    if isinstance(exception, MessageCantBeEdited):
        logging.info('message can\'t be edited')
        return True

    if isinstance(exception, MessageCantBeForwarded):
        logging.info('message can\'t be forwarded')
        return True

    if isinstance(exception, MessageNotModified):
        logging.info('message is not modified')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.info('Message text is empty')
        return True

    if isinstance(exception, MessageToEditNotFound):
        logging.info('message to edit not found')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.info('message to delete not found')
        return True

    if isinstance(exception, MessageToForwardNotFound):
        logging.info('message to forward not found')
        return True

    if isinstance(exception, CantGetUpdates):
        logging.info('can\'t use getUpdates method while webhook is active')
        return True

    if isinstance(exception, CantParseEntities):
        logging.info(f'can\'t parse entities. ExceptionArgs: {exception.args}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.info(f'Telegram API error: {update}')
        return True

    if isinstance(exception, BadRequest):
        logging.info(f'BadRequest. Exception: {exception}, update: {update}')
        return True

    if isinstance(exception, BotBlocked):
        logging.info(f'bot was blocked by the user. Update: {update}')
        return True

    if isinstance(exception, BotKicked):
        logging.info(f'bot was kicked from. Update: {update}')
        return True


def register_errors_handler(dp: Dispatcher):
    '''Регистрация хендлеров ошибок.'''
    dp.register_errors_handler(
        errors_handler
    )
