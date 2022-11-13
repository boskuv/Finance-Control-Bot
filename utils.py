import datetime
import re
import pytz


def get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом временной зоны МСК"""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def is_valid(input_expense):
    if re.match(r"(\+|\-)\d+", input_expense) is not None:
        return True
    else:
        return False
