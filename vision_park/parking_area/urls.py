from django.urls import path
from . import views

app_name = 'parking_area'


urlpatterns = [
    path('', views.index, name='parking_area'),
    path('get_parking_spaces/', views.get_parking_spaces, name='get_parking_spaces'),
]