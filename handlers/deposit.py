from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import (
    ChatType,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from states.deposit import DepositStates
import deposits
import exceptions


async def get_sum_of_deposits_for_year(msg: Message, state: FSMContext):
    """Пополнения за календарный год"""
    await state.finish()  # TODO: если state активен

    sum_deposit = deposits.get_sum_deposit_for_year()
    await msg.answer(f"За текущий год на счета поступило: {sum_deposit}")


# state=None
async def invite_to_choose_deposit_card(msg: Message, state: FSMContext):
    """Приглашение к выбору карты для пополнения"""
    await state.finish()  # TODO: если state активен

    keyboard = InlineKeyboardMarkup(row_width=3)
    cards = [
        "SBER",
        "TNK",
        "VTB",
    ]  # TODO: получение из БД + возможность добавления новых
    for card in cards:
        keyboard.insert(InlineKeyboardButton(text=card, callback_data=card))
    await state.set_state(DepositStates.GETTING_LIST_OF_CARDS)
    await msg.answer(f"Выберите карту пополнения: ", reply_markup=keyboard)


async def choose_deposit_card(call: CallbackQuery, state: FSMContext):
    """Выбор карты для пополнения"""
    await state.update_data(card=call.data)
    await state.set_state(DepositStates.CHOOSING_DEPOSIT_CARD)
    await call.answer(text="Опишите характер пополнения:", show_alert=True)


async def add_deposit_description(msg: Message, state: FSMContext):
    """Ввод описания пополнения"""
    description_of_deposit = msg.text
    await state.update_data(description=description_of_deposit.lower().strip())
    await state.set_state(DepositStates.CHOOSING_DEPOSIT_DESCRIPTION)
    await msg.answer(text="Введите сумму пополнения:")


async def push_deposit_to_db(msg: Message, state: FSMContext):
    """Добавление пополнения в БД"""
    states = await state.get_data()

    deposit_values_from_states = list(states.values())
    amount_of_deposit = msg.text  # TODO: check if valid
    deposit_values_from_states.append(amount_of_deposit)

    try:
        deposit = deposits.add_deposit(
            ",".join(deposit_values_from_states)
        )  # TODO: if not None
        answer_message = f"Добавлено пополнение: {deposit.amount} руб на карту {deposit.card} с описанием: '{deposit.description}'.\n\n"  # TODO: refactor
    except exceptions.NotCorrectMessage as e:
        answer_message = str(e)

    await msg.answer(answer_message)
    await state.finish()


def register_deposit(dp: Dispatcher):
    dp.register_message_handler(
        get_sum_of_deposits_for_year,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        commands=["sum_deposit"],
        state="*",
    )
    dp.register_message_handler(
        invite_to_choose_deposit_card,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        commands=["add_deposit"],
        state=None,
    )
    dp.register_callback_query_handler(
        choose_deposit_card,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        state=DepositStates.GETTING_LIST_OF_CARDS,
    )
    dp.register_message_handler(
        add_deposit_description,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        state=DepositStates.CHOOSING_DEPOSIT_CARD,
    )
    dp.register_message_handler(
        push_deposit_to_db,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        state=DepositStates.CHOOSING_DEPOSIT_DESCRIPTION,
    )


__all__ = ["register_deposit"]
