from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hi")

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("INFO ABOUT HELP")