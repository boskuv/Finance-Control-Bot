from aiogram import Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType, KeyboardButton, Message, ReplyKeyboardMarkup


async def start_handler(
    msg: Message,
):

    keyboard = ReplyKeyboardMarkup(
        one_time_keyboard=False,
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton("/sum_deposit"),
                KeyboardButton("/add_deposit"),
                KeyboardButton("/add_expense"),
                KeyboardButton("/add_limited_expense"),
            ],
            [
                KeyboardButton("/help"),
                KeyboardButton("/start"),  # stop
            ],
            [
                KeyboardButton("Share your contact", request_contact=True),
            ],
        ],
    )
    await msg.bot.send_message(
        chat_id=msg.chat.id,
        text="Check your keyboard below",
        reply_markup=keyboard,
    )


async def help_handler(
    msg: Message,
):

    await msg.bot.send_message(
        chat_id=msg.chat.id,
        text="""
        БОТ ДЛЯ УЧЕТА ФИНАНСОВ\n\n
        Добавить расход: /add_expense\n
        Добавить пополнение: /add_deposit\n
        Пополнения за текущий календарный год: /sum_deposit\n
        Сегодняшняя статистика: /today\n
        За текущий месяц: /month\n
        Последние внесённые расходы: /last_expenses
        """,
    )


def register_start(dp: Dispatcher):
    dp.register_message_handler(
        start_handler,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        commands=["start"],
        state="*",
    )
    dp.register_message_handler(
        help_handler,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        commands=["help"],
        state="*",
    )


__all__ = ["register_start"]
