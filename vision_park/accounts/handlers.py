from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from asgiref.sync import sync_to_async

from accounts.models import CustomUser

import accounts.keyboards as kb

handler_router = Router()


@handler_router.message(CommandStart())
async def start(message: types.Message):
    username = message.text.split()[-1]

    try:
        user = await sync_to_async(CustomUser.objects.get)(username=username)
        await message.answer(f"Welcome back, {user.username}!",
                             reply_markup=kb.main)
    except CustomUser.DoesNotExist:
        await message.answer("User not found. Please register first!")

@handler_router.message(F.text == '🌐Website')
async def get_link_website(message: Message):
    await message.answer('Here is the link to the website',
                         reply_markup=kb.link_website)