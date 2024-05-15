from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse

from .forms import RegisterForm, LoginForm
from recognize.models import Car, ParkingSession


class RegisterView(View):
    template_name = 'accounts/registration.html'
    register_form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="main")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"title": "Register new user",
                                                    "register_form": self.register_form_class})

    def post(self, request):
        register_form = self.register_form_class(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            username = register_form.cleaned_data["username"]
            messages.success(request, f"Congratulations " + username + "! Your account has been successfully created!")
            return redirect(to="main")
        return render(request, self.template_name, {"register_form": register_form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="main")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Nice to see you {user.username}!")
            return redirect(to="main")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        username = request.user.username
        logout(request)
        return render(request, "accounts/logout.html", {"title": "Logout user", "username": username})
        # redirect(to="main")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    try:
        template_name = 'accounts/password_reset.html'
        email_template_name = 'accounts/password_reset_email.html'
        html_email_template_name = 'accounts/password_reset_email.html'
        success_url = reverse_lazy('accounts:password_reset_done')
        success_message = "An email with instructions to reset your password has been sent to %(email)s."
        subject_template_name = 'accounts/password_reset_subject.txt'
    except Exception as err:
        print(f"Error sending email: {err}")


@login_required
def profile_add_car(request):
    if request.method == 'POST':
        if 'add_license_plate' in request.POST:
            car_license_plate = request.POST.get('add_license_plate')
            car = Car.objects.get(license_plate=car_license_plate)
            car.owner_id = request.user.id
            car.save()
            return redirect(to='accounts:profile')
        else:
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        user_cars = Car.objects.filter(owner=request.user)
        available_cars = Car.objects.filter(owner__isnull=True)
        context = {'user_profile': request.user, 'user_cars': user_cars,
                   'available_cars': available_cars}
        return render(request, 'accounts/profile_add_cars.html', context)


@login_required
def profile_action(request, pk):
    if request.method == 'POST':
        if 'delete_license_plate' in request.POST:
            try:
                car = get_object_or_404(Car, id=pk)
                car_session_parking = ParkingSession.objects.filter(car_id=pk, total_cost__gt=0).exists()
                if car_session_parking:
                    messages.error(request, 'Payment has already been registered for this car number.')
                else:
                    car.owner = None
                    car.save()
            except Car.DoesNotExist:
                messages.error(request, 'Car does not exist.')
            return redirect('accounts:profile')
        else:
            return redirect('accounts:profile')
    else:
        return redirect('accounts:profile')

# @login_required
# def profile(request):
#     resolved_view = resolve(request.path)
#     active_menu = resolved_view.app_name
#     return render(request, 'accounts/profile.html', {"active_menu": active_menu, "title": "User profile"})
