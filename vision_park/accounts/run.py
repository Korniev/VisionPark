import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import handler_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(handler_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')