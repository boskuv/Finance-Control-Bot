from aiogram.dispatcher.filters.state import StatesGroup, State


class DepositStates(StatesGroup):
    GETTING_LIST_OF_CARDS = State()
    CHOOSING_DEPOSIT_CARD = State()
    CHOOSING_DEPOSIT_DESCRIPTION = State()
