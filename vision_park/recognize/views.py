from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone, formats
from django.urls import resolve, reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Q

from .forms import ImageUploadForm
from .models import Car, ParkingSession
from finance.models import Pricing
from parking_area.models import ParkingSpace


@login_required
def main(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    # ваш код для обробки запиту тут
    return render(request, "recognize/main.html", {"active_menu": active_menu, "title": "Recognize"})


@login_required
def upload_out(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    context = {"active_menu": active_menu, "title": "CVM Recognize"}
    return render(request, "recognize/upload_out.html", context)


@login_required
def upload_in(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            # Зберігаємо зображення у файловій системі
            image_file = request.FILES['image']
            fs = FileSystemStorage(location='media/incoming/')
            filename = fs.save(image_file.name, image_file)
            uploaded_file_url = fs.url(filename)
            
            # # Зберігаємо шлях до зображення у базі даних
            # image = IncomingImage(image=uploaded_file_url)
            # image.save()
            
            # Розпізнаємо номери на зображенні
            recognized_area = uploaded_file_url
            recognized_symbols = uploaded_file_url
            # recognized_text = recognize_numbers(uploaded_file_url)
            recognized_text = "LA 80*90CA"
            
            # # Перенаправляємо користувача на сторінку з результатами
            # return HttpResponseRedirect(reverse('upload_in_results', args=(recognized_area, recognized_symbols, recognized_text)))
            # Повертаємо результати у шаблон
            return render(request, 'recognize/result_in.html', {'recognized_area': recognized_area, 'recognized_symbols': recognized_symbols,
                                                       'recognized_text': recognized_text})
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
