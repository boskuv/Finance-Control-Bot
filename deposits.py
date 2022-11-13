""" Работа с поступлениями средств — их добавление, удаление, ведение статистики"""
from typing import List, NamedTuple, Optional, Literal


import db.db as db
from utils import get_now_formatted

# import exceptions
# from categories import Categories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом депозите"""

    card: str
    amount: float
    description: str


class Deposit(NamedTuple):
    """Структура добавленного в БД нового расхода"""

    id: Optional[int]
    card: Literal["SBER", "TNK", "VTB"]
    amount: float
    description: str


def add_deposit(raw_message: str) -> Deposit:
    """Добавляет введеную трату в БД"""
    parsed_message = _parse_message(raw_message)
    db.insert(
        "deposit",
        {
            "card": parsed_message.card,
            "amount": parsed_message.amount,
            "created": get_now_formatted(),
            "description": parsed_message.description,
        },
    )
    return Deposit(
        id=None,
        card=parsed_message.card,
        amount=parsed_message.amount,
        description=parsed_message.description,
    )


def get_sum_deposit_for_year() -> float:
    """Получить сумму пополнений за год"""
    return db.fetchsumforcurrentyear("deposit")


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом поступлении"""
    card = raw_message.split(",")[0]
    description = raw_message.split(",")[1]
    amount = raw_message.split(",")[2]
    return Message(card=card, amount=amount, description=description)
