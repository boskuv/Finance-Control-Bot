import logging
from config import load_config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import expenses, deposits
from categories import Categories
from utils import FinCheckerState, is_valid
import exceptions

"""
TOREAD:
callback_data
https://telegra.ph/Zapusk-funkcij-v-bote-po-tajmeru-11-28
gui
skip_updates
"""

"""
TODO:
обработка ошибок
ORM
reogranize structure
token to ini
drop state if time is out of range
проверка статистики по расписанию
"""

config = load_config("bot.ini")
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

categories = Categories().get_all_categories()

# TODO: команды из keyboard, подсказки команд
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов:\n\n"
        "Добавить расход: /expense\n"
        "Добавить пополнение: /deposit\n"
        "Пополнения за текущий календарный год: /sum_deposit\n"
        # "Сегодняшняя статистика: /today\n"
        # "За текущий месяц: /month\n"
        # "Последние внесённые расходы: /expenses"
    )


@dp.message_handler(commands="sum_deposit")
async def get_sum_of_deposits_for_year(message: types.Message):
    """Пополнения за календарный год"""
    sum = deposits.get_sum_deposit_for_year()
    await message.answer(f"За текущий год на счета поступило: {sum}")


@dp.message_handler(commands="deposit", state=None)
async def invite_to_choose_deposit_card(message: types.Message, state: FSMContext):
    """Приглашение к выбору карты для пополнения"""
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    cards = [
        "VISA",
        "TNK",
        "MC",
        "MIR",
        "VTB",
    ]  # TODO: получение из БД + возможность добавления новых
    for card in cards:
        keyboard.insert(types.InlineKeyboardButton(text=card, callback_data=card))
    await FinCheckerState.getting_list_of_cards.set()
    await message.answer(f"Выберите карту пополнения: ", reply_markup=keyboard)


@dp.callback_query_handler(state=FinCheckerState.getting_list_of_cards)
async def add_deposit_card(call: types.CallbackQuery, state: FSMContext):
    """Выбор карты для пополнения"""
    await state.update_data(card=call.data)
    await FinCheckerState.choosing_deposit_card.set()
    await call.answer(text="Опишите характер пополнения:", show_alert=True)


@dp.message_handler(state=FinCheckerState.choosing_deposit_card)
async def add_deposit_description(message: types.Message, state: FSMContext):
    """Выбор описания пополнения"""
    description = message.text
    await state.update_data(description=description.lower().strip())
    await FinCheckerState.choosing_deposit_description.set()
    await message.answer(text="Введите сумму пополнения:")


@dp.message_handler(state=FinCheckerState.choosing_deposit_description)
async def push_deposit_to_db(message: types.Message, state: FSMContext):
    """Добавляет пополнение в БД"""
    states = await state.get_data()
    values_from_states = list(states.values())
    values_from_states.append(message.text)

    try:
        deposit = deposits.add_deposit(
            ",".join(values_from_states)
        )  # TODO: if not None
        answer_message = f"Добавлены пополнение: {deposit.amount} руб на карту {deposit.card} с описанием: '{deposit.description}'.\n\n"  # TODO: refactor
    except exceptions.NotCorrectMessage as e:
        answer_message = str(e)
    await message.answer(answer_message)
    await state.finish()


@dp.message_handler(commands="expense", state=None)
async def invite_to_choose_expense_category(message: types.Message):
    """Выводит категории трат расходов для выбора"""
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for category in categories:
        keyboard.insert(
            types.InlineKeyboardButton(
                text=category.get("name"), callback_data=category.get("codename")
            )
        )
    await FinCheckerState.getting_list_of_expense_categories.set()
    await message.answer("Выберите категорию трат:", reply_markup=keyboard)


@dp.callback_query_handler(
    text=[category.get("codename") for category in categories],
    state=FinCheckerState.getting_list_of_expense_categories,
)
async def push_expense_category(call: types.CallbackQuery, state: FSMContext):
    """Сохраняет выбранную категорию и предлагает ввести сумму траты"""
    await state.update_data(category=call.data)
    await FinCheckerState.choosing_expense_category.set()
    await call.answer(text="Введите затраченную сумму:", show_alert=True)


@dp.message_handler(state=FinCheckerState.choosing_expense_category)
async def push_expense_to_db(message: types.Message, state: FSMContext):
    """Добавляет введенную трату в БД"""
    states = await state.get_data()
    if is_valid(message.text):
        try:
            expense = expenses.add_expense(
                ",".join([states.get("category"), message.text])
            )
            answer_message = f"Добавлены траты: {expense.amount} руб в категории '{Categories().get_name_by_codename(expense.category_codename)}'.\n\n"
        except exceptions.NotCorrectMessage as e:
            answer_message = str(e)
    else:
        answer_message = (
            "Неверный формат ввода. Шаблон: '+/-sum. Например: +330 или -330.'"
        )
    await message.answer(answer_message)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
