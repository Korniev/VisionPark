from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.models import CustomUser
from parking_area.models import ParkingSpace


# class IncomingImage(models.Model):
#     image = models.ImageField(upload_to='incoming/')


class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(CustomUser, blank=True, on_delete=models.CASCADE, related_name='cars')
    # photo_car = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    # predict = models.FloatField(null=True)
    # PayPass = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.license_plate

    # def save(self, *args, **kwargs):
    #     if self.photo_car:
    #         self.car_number = self.photo_car.recognized_car_number
    #         self.predict = self.photo_car.accuracy
    #     super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("car_list", kwargs={"pk": self.pk})


class ParkingSession(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    parking_number = models.ForeignKey(ParkingSpace, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    end_session = models.BooleanField(default=False)
