from django.db import models

from accounts.models import CustomUser
from finance.models import Pricing
from parking_area.models import ParkingSpace


class Car(models.Model):
    license_plate = models.CharField(max_length=16, unique=True)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='cars')
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.license_plate


class ParkingSession(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    parking_number = models.ForeignKey(ParkingSpace, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    tarif = models.ForeignKey(Pricing, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='pricing')
    total_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    end_session = models.BooleanField(default=False)
