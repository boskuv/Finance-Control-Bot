import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import expenses
from categories import Categories
from utils import FinCheckerState, is_valid
import exceptions

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

categories = Categories().get_all_categories()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов:\n\n"
        "Добавить расход: /kb\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses")
	

@dp.message_handler(commands="kb", state=None)
async def get_keyboard(message: types.Message):
    """Выводит категории трат для выбора"""
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for category in categories:
        keyboard.insert(types.InlineKeyboardButton(text=category.get("name"), callback_data=category.get("codename")))
    await FinCheckerState.s1.set()
    await message.answer("Выберите категорию трат:", reply_markup=keyboard)


@dp.callback_query_handler(text=[category.get("codename") for category in categories], state=FinCheckerState.s1)
async def push_category(call: types.CallbackQuery, state: FSMContext):
    """Сохраняет выбранную категорию и предлагает ввести сумму траты"""
    await state.update_data(category=call.data)
    await FinCheckerState.s2.set()
    await call.answer(text="Введите затраченную сумму:", show_alert=True)
	

@dp.message_handler(state=FinCheckerState.s2)
async def push_purchase(message: types.Message, state: FSMContext):
    """Добавляет введенную трату в БД"""
    states = await state.get_data()
    if is_valid(message.text):
        try:
            expense = expenses.add_expense(",".join([states.get("category"), message.text])) # зачем возврат значения
            answer_message = (f"Добавлены траты: {expense.amount} руб на {expense.category_codename}.\n\n") # категория, а не codename!
        except exceptions.NotCorrectMessage as e:
            answer_message = (str(e))
    else:
        answer_message = ("Неверный формат ввода. Шаблон: '+/-sum. Например: +330 или -330.'")
    await message.answer(answer_message)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) # skip_updates?