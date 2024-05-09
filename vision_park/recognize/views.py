import os

import cv2
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone, formats
from django.urls import resolve, reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings

from .forms import ImageUploadForm
from .models import Car, ParkingSession
from parking_area.models import ParkingSpace

import sys

sys.path.append('/Users/korniev/GItHub/VisionPark')
from datascience.main_yolo5 import yolo_predictions, net


def main(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    # ваш код для обробки запиту тут
    return render(request, "recognize/main.html", {"active_menu": active_menu, "title": "Recognize"})


def upload_out(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    context = {"active_menu": active_menu, "title": "CVM Recognize"}
    return render(request, "recognize/upload_out.html", context)


def upload_in(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'incoming'))
            # fs = FileSystemStorage(location='media/incoming/')
            filename = fs.save(image_file.name, image_file)

            image_path = fs.path(filename)
            img = cv2.imread(image_path)
            result_img, recognized_text = yolo_predictions(img, net)

            result_filename = 'processed_' + filename
            cv2.imwrite(os.path.join(fs.location, result_filename), result_img)
            result_img_url = fs.url('incoming/' + result_filename)

            thumbnail_size = (300, 200)
            thumbnail = cv2.resize(img, thumbnail_size, interpolation=cv2.INTER_AREA)
            thumbnail_filename = 'thumbnail_' + filename
            cv2.imwrite(os.path.join(fs.location, thumbnail_filename), thumbnail)
            thumbnail_image = fs.url('incoming/' + thumbnail_filename)
            print("Thumbnail path:", thumbnail_image)

            return render(request, 'recognize/result_in.html', {
                'recognized_area': result_img_url,
                'recognized_image': thumbnail_image,
                'recognized_text': recognized_text
            })
    else:
        form = ImageUploadForm()
    return render(request, 'recognize/upload_in.html', {'form': form})


@login_required
def create_parking_session(request):
    if request.method == 'POST':
        # uploaded_file_url = request.POST.get('uploaded_file_url')
        license_plate = request.POST.get('recognized_text')
        # Знайти або створити новий автомобіль за номером
        car, created = Car.objects.get_or_create(license_plate=license_plate)

        # Перевіряємо, чи існує активний запис ParkingSession з таким номером
        active_session_exists = ParkingSession.objects.filter(car=car, end_session=False).exists()
        if active_session_exists:
            messages.error(request, 'The Parking Session for this Car is already open.')
            return render(request, 'recognize/result_in.html')

        # Отримати доступне паркомiсце
        parking_space = ParkingSpace.get_available_space()

        if parking_space:
            # Створити новий запис про початок парковочної сесiї
            parking_session = ParkingSession(car=car, parking_number=parking_space)
            print(parking_session)
            parking_session.save()
            # Оновлюємо статус парковочного місця
            parking_space.is_occupied = True
            parking_space.save()

            # Після оновлення перенаправляємо користувача на ту ж сторінку
            return redirect(to='recognize:main')

        else:
            # Якщо паркомісця немає, показуємо повідомлення про це
            messages.error(request, 'No available parking space.')
            return render(request, 'recognize/result_in.html')

    else:
        return redirect('recognize:upload_in')


"""
def create_parking_session(request):
    if request.method == 'POST':
        # uploaded_file_url = request.POST.get('uploaded_file_url')
        license_plate = request.POST.get('recognized_text')
        # Знайти або створити новий автомобіль за номером
        car, created = Car.objects.get_or_create(license_plate=license_plate)

        # Перевіряємо, чи існує активний запис ParkingSession з таким номером
        active_session_exists = ParkingSession.objects.filter(car=car, end_session=False).exists()
        if active_session_exists:
            messages.error(request, 'The Parking Session for this Car is already open.')
            return render(request, 'recognize/result_in.html')

        # Отримати доступне паркомiсце
        parking_space = ParkingSpace.get_available_space()

        if parking_space:
            # Створити новий запис про початок парковочної сесiї
            parking_session = ParkingSession(car=car, parking_number=parking_space)
            print(parking_session)
            parking_session.save()
            # Оновлюємо статус парковочного місця
            parking_space.is_occupied = True
            parking_space.save()

            # Після оновлення перенаправляємо користувача на ту ж сторінку
            return redirect(to='recognize:main')

        else:
            # Якщо паркомісця немає, показуємо повідомлення про це
            messages.error(request, 'No available parking space.')
            return render(request, 'recognize/result_in.html')

    else:
        return redirect('recognize:upload_in')
"""
