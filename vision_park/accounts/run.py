import asyncio
import django
import os
import logging

from aiogram import Bot, Dispatcher

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vision_park.settings")
django.setup()

from .config import TOKEN
from .handlers import handler_router
from .queries_bot import second_router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(handler_router)
    dp.include_router(second_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
