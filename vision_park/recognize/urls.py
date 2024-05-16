from django.urls import path
from . import views

app_name = "recognize"

urlpatterns = [
    path("main", views.main, name="main"),
    path("upload_in", views.upload_in, name="upload_in"),
    path("result_in", views.create_parking_session, name="result_in"),
    path("session_view", views.session_view, name="session_view"),
    path('session_action/<int:pk>/', views.session_action, name='session_action'),
    path("download_csv", views.download_csv, name="download_csv"),
]
