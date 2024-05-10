from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import ParkingSpace


#@login_required
def index(request):
    parking_spaces = ParkingSpace.objects.all()

    total_parking_spaces = parking_spaces.count()
    free_spaces = parking_spaces.filter(is_occupied=False).count()
    occupied_spaces = total_parking_spaces - free_spaces

    data = {
        'total_parking_spaces': total_parking_spaces,
        'free_spaces': free_spaces,
        'parking_progress': int((occupied_spaces / total_parking_spaces) * 100)
    }
    return render(request, 'parking_area/parking_area.html', context=data)


#@login_required
def get_parking_spaces(request):
    parking_spaces = ParkingSpace.objects.all().order_by('id').values('number', 'is_occupied')
    # print(parking_spaces)
    return JsonResponse(list(parking_spaces), safe=False)
