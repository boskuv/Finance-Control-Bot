from aiogram.dispatcher.filters.state import StatesGroup, State


class ExpenseStates(StatesGroup):
    GETTING_LIST_OF_EXPENSE_CATEGORIES = State()
    CHOOSING_EXPENSE_CATEGORY = State()
    ENTERING_LIMITED_EXPENSE = State()
