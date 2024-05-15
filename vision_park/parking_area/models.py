from django.db import models


class ParkingSpace(models.Model):
    number = models.CharField(max_length=10, unique=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.number

    @classmethod
    def get_available_space(cls):
        sequence = ['A01', 'B02', 'A03', 'B04', 'A05', 'B06', 'A07', 'B08', 'A09', 'B10',
                    'A02', 'B01', 'A04', 'B03', 'A06', 'B05', 'A08', 'B07', 'A10', 'B09', ]
        for space in sequence:
            try:
                parking_space = cls.objects.get(number=space, is_occupied=False)
                return parking_space
            except cls.DoesNotExist:
                continue
        return None
