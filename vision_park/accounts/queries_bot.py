from aiogram.filters import CommandStart
from aiogram import types
from asgiref.sync import sync_to_async

from finance.models import Pricing
from parking_area.models import ParkingSpace
from .handlers import handler_router
from .models import CustomUser


@handler_router.message(CommandStart(commands=['mycars']))
async def get_user_cars(message: types.Message):
    username = message.from_user.username
    try:
        user = await sync_to_async(CustomUser.objects.get)(telegram_nickname=username)
        cars = await sync_to_async(list)(user.cars.all())
        car_plates = [car.license_plate for car in cars]
        await message.answer("Your cars: " + ", ".join(car_plates))
    except CustomUser.DoesNotExist:
        await message.answer("User not found. Please register first!")


@handler_router.message(CommandStart(commands=['price']))
async def get_parking_price(message: types.Message):
    pricing_info = await sync_to_async(Pricing.objects.first)()
    if pricing_info:
        await message.answer(f"Current parking price: ${pricing_info.cost_per_hour} per hour")
    else:
        await message.answer("No pricing information available.")


@handler_router.message(CommandStart(commands=['available']))
async def check_available_parking(message: types.Message):
    available_space = await sync_to_async(ParkingSpace.get_available_space)()
    if available_space:
        await message.answer(f"Parking space {available_space.number} is available.")
    else:
        await message.answer("No available parking spaces.")
