import logging
from config import load_config

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import expenses, deposits
from categories import Categories
from utils import is_valid
import exceptions
from handlers.start import register_start

"""
TOREAD:
callback_data
https://telegra.ph/Zapusk-funkcij-v-bote-po-tajmeru-11-28
gui
skip_updates
ChatTypeFilter(chat_type=ChatType.PRIVATE)
chat_id=msg.chat.id
KeyboardButton("Share your contact", request_contact=True)
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType
"""

"""
TODO:
обработка ошибок (запущено 2 бота) и др.
ORM
drop state if time is out of range
проверка статистики по расписанию
logging
эмодзи
имена кнопок вместо команд
methods naming
фильтрация пользователей
Description in English
"""


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # logger.error("Starting bot")
    config = load_config("bot.ini")

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)

    register_start(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


categories = Categories().get_all_categories()


# @dp.message_handler(commands="expense", state=None)
# async def invite_to_choose_expense_category(message: types.Message):
#     """Выводит категории трат расходов для выбора"""
#     keyboard = types.InlineKeyboardMarkup(row_width=3)
#     for category in categories:
#         keyboard.insert(
#             types.InlineKeyboardButton(
#                 text=category.get("name"), callback_data=category.get("codename")
#             )
#         )
#     await FinCheckerState.getting_list_of_expense_categories.set()
#     await message.answer("Выберите категорию трат:", reply_markup=keyboard)


# @dp.callback_query_handler(
#     text=[category.get("codename") for category in categories],
#     state=FinCheckerState.getting_list_of_expense_categories,
# )
# async def push_expense_category(call: types.CallbackQuery, state: FSMContext):
#     """Сохраняет выбранную категорию и предлагает ввести сумму траты"""
#     await state.update_data(category=call.data)
#     await FinCheckerState.choosing_expense_category.set()
#     await call.answer(text="Введите затраченную сумму:", show_alert=True)


# @dp.message_handler(state=FinCheckerState.choosing_expense_category)
# async def push_expense_to_db(message: types.Message, state: FSMContext):
#     """Добавляет введенную трату в БД"""
#     states = await state.get_data()
#     if is_valid(message.text):
#         try:
#             expense = expenses.add_expense(
#                 ",".join([states.get("category"), message.text])
#             )
#             answer_message = f"Добавлены траты: {expense.amount} руб в категории '{Categories().get_name_by_codename(expense.category_codename)}'.\n\n"
#         except exceptions.NotCorrectMessage as e:
#             answer_message = str(e)
#     else:
#         answer_message = (
#             "Неверный формат ввода. Шаблон: '+/-sum. Например: +330 или -330.'"
#         )
#     await message.answer(answer_message)
#     await state.finish()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass  # logger.error("Bot stopped!")
