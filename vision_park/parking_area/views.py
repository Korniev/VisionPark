import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import localtime

from django.utils import timezone,formats


def index(request):
    #sessions = ParkingSession.objects.filter(user=request.user).order_by('-start_time')
    # return render(request, 'parking_area/parking_area.html', {'sessions': sessions})
    return render(request, 'parking_area/parking_area.html')
