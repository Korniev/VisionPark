from aiogram import Router, types
# from aiogram.types import Message
from aiogram.filters import CommandStart

from accounts.models import CustomUser

handler_router = Router()


@handler_router.message(CommandStart())
async def start(message: types.Message):
    username = message.text.split()[-1]

    try:
        user = CustomUser.objects.get(username=username)
        await message.answer(f"Welcome back, {user.username}!")
    except CustomUser.DoesNotExist:
        await message.answer("User not found. Please register first!")
