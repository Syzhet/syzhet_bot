from typing import Dict, List, Union

from aiogram import types


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
             f'updated: {resp["updated_on"]}\n'
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

    for resp in response:
        await message.answer(
            (f'id заказа: {resp["id"]}\n'
             f'title: {resp["title"]}\n'
             f'description: {resp["description"]}\n'
             'Пользователь:\n'
             f'id пользователя: {resp["user"]["id"]}\n'
             f'usernmae: @{resp["user"]["username"]}\n'
             f'telegram_id: {resp["user"]["telegram_id"]}\n'
             f'updated: {resp["user"]["updated_on"]}\n'
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
    await message.answer(
        (f'id пользователя: {response["id"]}\n'
         f'usernmae: @{response["username"]}\n'
         f'telegram_id: {response["telegram_id"]}\n'
         f'updated: {response["updated_on"]}\n'
         f'Заказы:\n{orders}')
    )
