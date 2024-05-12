from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path('payments-user/', views.payments_user, name='payments_user'),
    path('payment-preview/<int:session_id>/', views.payment_preview, name='payment_preview'),
    path('payment-confirm/<int:session_id>/', views.payment_confirm, name='payment_confirm'),
    path('tariffs/', views.tariffs, name='tariffs'),
    path('tariff-add/', views.tariff_add, name='tariff_add'),
    path('tariff-complete/<int:tariff_id>', views.tariff_complete, name='tariff_complete'),
]