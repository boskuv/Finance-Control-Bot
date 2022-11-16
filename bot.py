import logging
from config import load_config

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from handlers.start import register_start
from handlers.deposit import register_deposit
from handlers.expense import register_expense

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
    register_deposit(dp)
    register_expense(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass  # logger.error("Bot stopped!")
