from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import ParkingSpace
from recognize.models import ParkingSession


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
    if request.user.is_authenticated:
        user_parking_sessions = ParkingSession.objects.filter(car__owner=request.user, end_session=False)

        parking_spaces_info = []
        for session in user_parking_sessions:
            parking_space_info = {
                'user_parking_number': session.parking_number.number,
            }
            parking_spaces_info.append(parking_space_info)
    else:
        parking_spaces_info = []
    print(parking_spaces_info)

    parking_spaces = ParkingSpace.objects.all().order_by('id').values('number', 'is_occupied')
    print(parking_spaces)

    response_data = {
        'user_parking_spaces': parking_spaces_info,
        'all_parking_spaces': list(parking_spaces),
    }
    return JsonResponse(response_data, safe=False)
