from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.profile_add_car, name='profile'),
    # path('add_car/', views.profile_add_car, name='add_car'),
#     path('add-car/', views.add_car, name='add_car'),
#     path('delete/<int:pk>', views.delete, name='delete'),
#     path('edit-car/<int:pk>/', views.edit_car, name='edit_car'),
#     path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                          success_url='/auth/reset-password/complete/'),
                                          name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
                                           name='password_reset_complete'),
]