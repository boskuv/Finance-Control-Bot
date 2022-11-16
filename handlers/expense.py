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

from states.expense import ExpenseStates
import expenses
from categories import Categories
from utils import is_valid
import exceptions


categories = Categories().get_all_categories()


async def invite_to_choose_expense_category(msg: Message, state: FSMContext):
    """Выводит категории трат расходов для выбора"""
    await state.finish()

    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in categories:
        keyboard.insert(
            InlineKeyboardButton(
                text=category.get("name"), callback_data=category.get("codename")
            )
        )
    await state.set_state(ExpenseStates.GETTING_LIST_OF_EXPENSE_CATEGORIES)
    await msg.answer("Выберите категорию трат:", reply_markup=keyboard)


async def choose_expense_category(call: CallbackQuery, state: FSMContext):
    """Сохраняет выбранную категорию и предлагает ввести сумму траты"""
    await state.update_data(category=call.data)
    await state.set_state(ExpenseStates.CHOOSING_EXPENSE_CATEGORY)
    await call.answer(text="Введите затраченную сумму:", show_alert=True)


async def push_expense_to_db(msg: Message, state: FSMContext):
    """Добавляет введенную трату в БД"""
    states = await state.get_data()
    if is_valid(msg.text):
        try:
            expense = expenses.add_expense(",".join([states.get("category"), msg.text]))
            answer_message = f"Добавлены траты: {expense.amount} руб в категории '{Categories().get_name_by_codename(expense.category_codename)}'.\n\n"
        except exceptions.NotCorrectMessage as e:
            answer_message = str(e)
    else:
        answer_message = (
            "Неверный формат ввода. Шаблон: '+/-sum. Например: +330 или -330.'"
        )
    await msg.answer(answer_message)
    await state.finish()


def register_expense(dp: Dispatcher):
    dp.register_message_handler(
        invite_to_choose_expense_category,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        commands=["add_expense"],
        state=None,
    )
    dp.register_callback_query_handler(  # TODO: text=[category.get("codename") for category in categories],
        choose_expense_category,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        state=ExpenseStates.GETTING_LIST_OF_EXPENSE_CATEGORIES,
    )
    dp.register_message_handler(
        push_expense_to_db,
        ChatTypeFilter(chat_type=ChatType.PRIVATE),
        state=ExpenseStates.CHOOSING_EXPENSE_CATEGORY,
    )


__all__ = ["register_expense"]
