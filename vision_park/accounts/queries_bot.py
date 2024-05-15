from aiogram.filters import CommandStart
from aiogram import types, F, Router
from asgiref.sync import sync_to_async

from finance.models import Pricing
from parking_area.models import ParkingSpace

from .models import CustomUser

second_router = Router()


@second_router.message(F.text == '🚘My cars')
async def get_user_cars(message: types.Message):
    username = message.from_user.username
    try:
        user = await sync_to_async(CustomUser.objects.get)(telegram_nickname=username)
        cars = await sync_to_async(list)(user.cars.all())
        car_plates = [car.license_plate for car in cars]
        await message.answer("Your cars: " + ", ".join(car_plates))
    except CustomUser.DoesNotExist:
        await message.answer("User not found. Please register first!")


@second_router.message(F.text == '💲Price')
async def get_parking_price(message: types.Message):
    pricing_info = await sync_to_async(Pricing.objects.first)()
    if pricing_info:
        await message.answer(f"Current parking price: ${pricing_info.cost_per_hour} per hour")
    else:
        await message.answer("No pricing information available.")


@second_router.message(F.text == 'ℹ️Available parking')
async def check_available_parking(message: types.Message):
    available_spaces = await sync_to_async(ParkingSpace.objects.filter(is_occupied=False).count)()
    if available_spaces > 0:
        await message.answer(f"{available_spaces} parking spaces are available.")
    else:
        await message.answer("No available parking spaces.")

