from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from asgiref.sync import sync_to_async
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from .config import ADMIN

from accounts.models import CustomUser

import accounts.keyboards as kb

handler_router = Router()


class Support(StatesGroup):
    info = State()


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


@handler_router.message(F.text == '🙌Support')
@handler_router.message(Command('Support'))
async def support_button_pressed(message: types.Message, state=FSMContext):
    await state.set_state(Support.info)
    await message.answer(
        'Write what happened and leave the phone number in one message. Support will contact you by phone shortly')


@handler_router.message(Support.info)
async def info_for_support(message: Message, state: FSMContext):
    await state.clear()
    admin_id = ADMIN
    await message.bot.send_message(admin_id,
                                   f"New message from user {message.from_user.username} ({message.from_user.id}):\n\n{message.text}")
