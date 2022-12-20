from datetime import datetime, timedelta
from typing import Dict, List, Union

from aiogram import types


def to_timezone(date_str: str) -> str:
    reg_date = datetime.fromisoformat(date_str)
    reg_date_no_ms = reg_date.replace(microsecond=0)
    reg_date_for_message = reg_date_no_ms + timedelta(hours=3)
    return reg_date_for_message.strftime('%d.%m.%Y %H:%M')


async def list_user_to_message(
    message: types.Message,
    response: List
) -> None:
    """
    Функция подготовки данных и формирования текста
    для отправки сообщения администратору бота
    по зарегистрированным пользователям.
    """

    for resp in response:
        updated = to_timezone(resp["updated_on"])
        orders: Union[str, List] = []
        if resp['orders']:
            for ord in resp['orders']:
                orders.append(
                    (f'id заказа: {ord["id"]}\n'
                     f'Название: {ord["title"]}\n'
                     f'Описание: {ord["description"]}\n'
                     '-----------\n')
                )
            orders = ''.join(orders)
        else:
            orders = 'Нет заказов'
        await message.answer(
            (f'id пользователя: {resp["id"]}\n'
             f'usernmae: @{resp["username"]}\n'
             f'telegram_id: {resp["telegram_id"]}\n'
             f'updated: {updated}\n'
             f'Заказы:\n{orders}')
        )


async def list_order_to_message(
    message: types.Message,
    response: List
) -> None:
    """
    Функция подготовки данных и формирования текста
    для отправки сообщения администратору бота по заказам работ.
    """
    if not response:
        await message.answer('В базе нет заказов!')
    for resp in response:
        updated = to_timezone(resp["user"]["updated_on"])
        await message.answer(
            (f'id заказа: {resp["id"]}\n'
             f'title: {resp["title"]}\n'
             f'description: {resp["description"]}\n'
             'Пользователь:\n'
             f'id пользователя: {resp["user"]["id"]}\n'
             f'usernmae: @{resp["user"]["username"]}\n'
             f'telegram_id: {resp["user"]["telegram_id"]}\n'
             f'updated: {updated}\n'
             '-----------\n')
        )


async def user_obj_to_message(
    message: types.Message,
    response: Dict
) -> None:
    """
    Функция подготовки данных и формирования текста
    для отправки сообщения администратору бота
    по конкретному зарегистрированному пользователю.
    """

    orders: Union[str, List] = []
    if response['orders']:
        for ord in response['orders']:
            orders.append(
                (f'id заказа: {ord["id"]}\n'
                    f'Название: {ord["title"]}\n'
                    f'Описание: {ord["description"]}\n'
                    '-----------\n')
            )
        orders = ''.join(orders)
    else:
        orders = 'Нет заказов'
    updated = to_timezone(response["updated_on"])
    await message.answer(
        (f'id пользователя: {response["id"]}\n'
         f'usernmae: @{response["username"]}\n'
         f'telegram_id: {response["telegram_id"]}\n'
         f'updated: {updated}\n'
         f'Заказы:\n{orders}')
    )


async def order_obj_to_message(
    message: types.Message,
    response: Dict
):
    """
    Функция подготовки данных и формирования текста
    для отправки сообщения администратору бота
    по конкретному заказу.
    """

    updated = to_timezone(response["user"]["updated_on"])
    await message.answer(
        (f'id заказа: {response["id"]}\n'
         f'title: {response["title"]}\n'
         f'description: {response["description"]}\n'
         'Пользователь:\n'
         f'id пользователя: {response["user"]["id"]}\n'
         f'usernmae: @{response["user"]["username"]}\n'
         f'telegram_id: {response["user"]["telegram_id"]}\n'
         f'updated: {updated}\n')
        )
