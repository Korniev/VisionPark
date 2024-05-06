from django.urls import path
from . import views

app_name = 'parking_area'


urlpatterns = [
    path('', views.index, name='parking_area'),
]