from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone, formats
from django.urls import resolve, reverse
from django.contrib import messages

from .forms import TariffForm
from .models import Pricing
from recognize.models import Car, ParkingSession


@login_required
def payments_user(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    car = Car.objects.filter(owner=request.user)
    sessions = ParkingSession.objects.filter(car__in=car).order_by('-start_time')
    # sessions = ParkingSession.objects.filter(car__in=car).select_related('tarif')
    return render(request, 'finance/payments_user.html',
                  {"active_menu": active_menu, "title": "Finance", "sessions": sessions})


@login_required
def payment_preview(request, session_id):
    session = get_object_or_404(ParkingSession, id=session_id)
    if request.method == 'POST':
        if request.user.username == session.car.owner.username:
            total_cost = request.POST.get('total_cost')
            if total_cost:
                session.total_cost = total_cost
                session.end_time = timezone.now()
                session.save()
                return redirect(to='finance:payment_confirm', session_id=session_id)
        else:
            messages.error(request, 'Ви не можете підтвердити оплату для цього сеансу паркування.')
            return redirect(to='finance:payment_preview', session_id=session_id)
    else:
        wasted_time = (timezone.now() - session.start_time).total_seconds() / 60
        cost_per_hour = Decimal(session.tarif.cost_per_hour) if isinstance(session.tarif.cost_per_hour,
                                                                           float) else session.tarif.cost_per_hour
        total_cost = max(0, cost_per_hour * Decimal((wasted_time - session.tarif.free_period) / 60))
        context = {'session': session, 'total_cost': total_cost, }

        return render(request, 'finance/payment_preview.html', context)


@login_required
def payment_confirm(request, session_id):
    session = get_object_or_404(ParkingSession, id=session_id)
    return render(request, 'finance/payment_confirm.html', {'session': session})


@login_required
def tariffs(request):
    resolved_view = resolve(request.path)
    active_menu = resolved_view.app_name
    tariffs = Pricing.objects.all().order_by('-start_time')
    return render(request, 'finance/tariffs.html', {"active_menu": active_menu, "title": "Finance", "tariffs": tariffs})


@login_required
def tariff_complete(request, tariff_id):
    tariff = get_object_or_404(Pricing, id=tariff_id)
    if request.method == 'POST':
        print(request.POST)
        if request.user.is_superuser:
            end_time = request.POST.get('end_time')
            if end_time == "complete":
                tariff.end_time = timezone.now()
                tariff.save()
                messages.success(request, 'Tariff has been expired.')
                return redirect(to='finance:tariffs')
        else:
            messages.error(request, 'You do not have the rights to change tariffs.')
            return redirect(to='finance:tariff_complete', tariff_id=tariff_id)
    else:
        resolved_view = resolve(request.path)
        active_menu = resolved_view.app_name
        context = {'active_menu': active_menu, 'tariff': tariff}
        return render(request, 'finance/tariff_complete.html', context)


@login_required
def tariff_add(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = TariffForm(request.POST)
            if form.is_valid():
                current_time = timezone.now()
                start_of_day = current_time.replace(hour=0, minute=0, second=1)
                tariff = form.save(commit=False)
                tariff.start_time = start_of_day
                tariff.save(force_insert=True)
                messages.success(request, 'Tariff created successfully.')
                return redirect(to='finance:tariffs')
        else:
            messages.error(request, 'You do not have the rights to create tariff.')
            return redirect(to='finance:tariff_add')
    else:
        form = TariffForm()
        return render(request, 'finance/tariff_add.html', {'form': form})
