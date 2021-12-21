from aiogram.dispatcher.filters.state import State, StatesGroup

import re

class FinCheckerState(StatesGroup):
    s1 = State()
    s2 = State()

def is_valid(input_expense):
    if re.match(r'(\+|\-)\d+', input_expense) is not None:
        return True
    else:
        return False