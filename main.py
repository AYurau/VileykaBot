import asyncio

from aiogram import Bot, Dispatcher, executor

from Base import *
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


loop = asyncio.get_event_loop()
bot = Bot(TOKEN,parse_mode = 'HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp) #Запросы к телеграмму
    loop = asyncio.get_event_loop()
    loop.run_until_complete(await_req())
    loop.close()

