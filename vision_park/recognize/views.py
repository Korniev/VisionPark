
import json

import cv2
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import resolve
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Q
from django.conf import settings


from django.utils import timezone,formats
import os
import csv
from datetime import datetime


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve, reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect

from .forms import ImageUploadForm
from .models import Car, ParkingSession
from finance.models import Pricing
from parking_area.models import ParkingSpace

import cv2
from utils.datascience.main_yolo5 import yolo_predictions, net


@login_required
def main(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    return render(request, "recognize/main.html", {"active_menu": active_menu, "title": "Recognize"})


@login_required
def upload_out(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    context = {"active_menu": active_menu, "title": "CVM Recognize"}
    return render(request, "recognize/upload.html", context)

    return render(request, "recognize/upload_out.html", context)


@login_required
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
        if car.is_blocked:
            messages.error(request, 'This Сar is not allowed to enter the parking\n"Ase of Base".')
            return render(request, 'recognize/result_in.html')

        # Перевіряємо, чи існує активний запис ParkingSession з таким номером
        active_session_exists = ParkingSession.objects.filter(car=car, end_session=False).exists()
        if active_session_exists:
            messages.error(request, 'The Parking Session for this Car is already open.')
            return render(request, 'recognize/result_in.html')

        # Отримати доступне паркомiсце
        parking_space = ParkingSpace.get_available_space()

        if parking_space:
            # Створити новий запис про початок парковочної сесiї
            tarif_id = tariff_insert(request)
            parking_session = ParkingSession(car=car, parking_number=parking_space, tarif_id=tarif_id)
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


@login_required
def tariff_insert(request):
    # Отримуємо тариф з найбільшим <start_time>, де <end_time> є [None]
    tariff = Pricing.objects.filter(Q(end_time__isnull=True)).order_by('-start_time').first()
    # Якщо такий тариф існує, отримуємо його <id>
    if tariff:
        tariff_id = tariff.id
    else:
        # Якщо такий тариф не знайдено, беремо тариф з <id> = 1 за замовчуванням
        default_tariff = Pricing.objects.get(id=1)
        tariff_id = default_tariff.id
    return tariff_id

  
@login_required
def session_view(request):
    # Виконуємо [JOIN] таблиці [Car] з таблицею [ParkingSession] за допомогою [select_related]
    # де <car> - назва стовпця якiй є iдентифiкатором моделi (таблицi) [Car]
    # Також виконуємо з'єднання з моделю (таблицею) [CustomUser] через модель (таблицю) [Car]
    # sessions_parking = ParkingSession.objects.filter(end_session=False).order_by('-start_time')[:20].select_related('car')
    sessions_parking = ParkingSession.objects.filter(Q(end_session=False) | Q(car__is_blocked=True)
                                                    ).order_by('-start_time')[:20].select_related('car')
    # Без зв'язку [related] у моделi [Car] через <owner> було б так:
    # sessions_parking = ParkingSession.objects.filter(end_session=False).order_by('-start_time')[:20].select_related('car__owner')
    return render(request, 'recognize/session_view.html', {'sessions_parking': sessions_parking})


@login_required
def session_action(request, pk):
    if request.method == 'POST':
        if request.user.is_superuser:
            if 'close_session' in request.POST:
                session_parking = get_object_or_404(ParkingSession.objects.select_related('tarif'), id=pk)
                time_difference_minutes = (timezone.now() - session_parking.start_time).total_seconds() / 60
                if time_difference_minutes <= session_parking.tarif.free_period:
                    session_parking.end_session = True
                    session_parking.save()
                    parking_space = get_object_or_404(ParkingSpace, id=session_parking.parking_number_id)
                    parking_space.is_occupied = False
                    parking_space.save()
                    messages.success(request, 'Parking has been successfully completed.')
                else:
                    messages.error(request, 'The free parking time has been exceeded.')
            elif 'unblock' in request.POST:
                session_parking = get_object_or_404(ParkingSession, id=pk)
                car = get_object_or_404(Car, id=session_parking.car.id)
                car.is_blocked = False
                car.save()
            elif 'ban' in request.POST:
                session_parking = get_object_or_404(ParkingSession, id=pk)
                car = get_object_or_404(Car, id=session_parking.car.id)
                car.is_blocked = True
                car.save()
            return HttpResponseRedirect(reverse('recognize:session_view'))
    return HttpResponseRedirect(reverse('recognize:session_view'))


@login_required
def session_action(request, pk):
    if request.method == 'POST':
        if request.user.is_superuser:
            if 'close_session' in request.POST:
                session_parking = get_object_or_404(ParkingSession.objects.select_related('tarif'), id=pk)
                time_difference_minutes = (timezone.now() - session_parking.start_time).total_seconds() / 60
                if time_difference_minutes <= session_parking.tarif.free_period:
                    session_parking.end_session = True
                    session_parking.save()
                    parking_space = get_object_or_404(ParkingSpace, id=session_parking.parking_number_id)
                    parking_space.is_occupied = False
                    parking_space.save()
                    messages.success(request, 'Parking has been successfully completed.')
                else:
                    messages.error(request, 'The free parking time has been exceeded.')
            elif 'unblock' in request.POST:
                session_parking = get_object_or_404(ParkingSession, id=pk)
                car = get_object_or_404(Car, id=session_parking.car.id)
                car.is_blocked = False
                car.save()
            elif 'ban' in request.POST:
                session_parking = get_object_or_404(ParkingSession, id=pk)
                car = get_object_or_404(Car, id=session_parking.car.id)
                car.is_blocked = True
                car.save()
            return HttpResponseRedirect(reverse('recognize:session_view'))
    return HttpResponseRedirect(reverse('recognize:session_view'))


def save_to_csv(user, object_data):
    current_date = datetime.now().strftime("%Y-%m-%d")  # форматує дату у форматі <YYYY-MM-DD>
    filename = f"{user}-{current_date}.csv"
    file_path = settings.MEDIA_ROOT / filename

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # Записуємо заголовки CSV
        writer.writerow(['User', 'Email', 'Phone', 'License Plate', 'Status', 'Start parking',
                         'Number parkingplace', 'Tariff', 'Free Period', 'Payment', 'End parking',
                         'Close session'])
        for data in object_data:
            if data.car.owner:
                writer.writerow([data.car.owner, data.car.owner.email, data.car.owner.phone_number,
                                data.car.license_plate, data.car.is_blocked, data.start_time, data.parking_number,
                                data.tarif.name , data.tarif.free_period, data.total_cost, data.end_time,
                                data.end_session])
            else:
                writer.writerow(["", "", "",
                                data.car.license_plate, data.car.is_blocked, data.start_time, data.parking_number,
                                data.tarif.name , data.tarif.free_period, data.total_cost, data.end_time,
                                data.end_session])

    return filename


# Використовується зовнішня функція [save_to_csv], визначена раніше
@login_required
def download_csv(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            if 'download_csv' in request.POST:
                sessions_parking = ParkingSession.objects.all().order_by('start_time').select_related('car')
                print(sessions_parking)
                filename = save_to_csv(request.user.username, sessions_parking)
                messages.success(request, f'The file {filename} was\nsuccessfully saved to the /media directory.')
            return HttpResponseRedirect(reverse('recognize:session_view'))
    return HttpResponseRedirect(reverse('recognize:session_view'))
