from django.db import models


class Pricing(models.Model):
    name = models.CharField(max_length=50)
    free_period = models.PositiveIntegerField()
    cost_per_hour = models.DecimalField(max_digits=5, decimal_places=2)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
