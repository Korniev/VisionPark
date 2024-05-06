from django.contrib.auth.models import AbstractUser
from django.db import models

# from cars.models import Car
# from photos.models import Photo



class CustomUser(AbstractUser):
    username = models.CharField(max_length=32, blank=False, unique=True)
    # first_name = models.CharField(max_length=32, required=False)
    # last_name = models.CharField(max_length=32, required=False) 
    email = models.EmailField(max_length=64, blank=False, unique=True)
    phone_number = models.CharField(null=True, unique=True) 
    telegram_nickname = models.CharField(max_length=32, blank=True, unique=True)
    # telegram_id = models.CharField(max_length=64, required=False)
 
    def __str__(self):
        return self.username



class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cars')
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