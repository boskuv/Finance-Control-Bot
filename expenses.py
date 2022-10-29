""" Работа с расходами — их добавление, удаление, ведение статистики"""
from typing import List, NamedTuple, Optional


from utils import get_now_formatted
import db

# import exceptions
# from categories import Categories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""

    amount: float
    category_codename: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""

    id: Optional[int]
    amount: float
    category_codename: str


def add_expense(raw_message: str) -> Expense:
    """Добавляет введеную трату в БД"""
    parsed_message = _parse_message(raw_message)
    db.insert(
        "expense",
        {
            "amount": parsed_message.amount,
            "created": get_now_formatted(),
            "category_codename": parsed_message.category_codename,
        },
    )
    return Expense(
        id=None,
        amount=parsed_message.amount,
        category_codename=parsed_message.category_codename,
    )


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    category_codename = raw_message.split(",")[0]
    amount = raw_message.split(",")[1]
    return Message(amount=amount, category_codename=category_codename)
