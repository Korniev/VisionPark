from django.urls import path
from . import views

app_name = "recognize"

urlpatterns = [
    # path("", views.main, name="main"),
    # path("", views.main, name="index"),
    path("main", views.main, name="main"),
    path("upload_in", views.upload_in, name="upload_in"),
    path("result_in", views.create_parking_session, name="result_in"),
    path("upload_out", views.upload_out, name="upload_out"),
]