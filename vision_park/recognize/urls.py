from django.urls import path
from . import views

app_name = "recognize"

urlpatterns = [
    # path("", views.main, name="main"),
    # path("", views.main, name="index"),
    path("main", views.main, name="main"),
    path("upload", views.upload_file, name="upload"),
]