from django import forms
from .models import Pricing


class TariffForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ['name', 'free_period', 'cost_per_hour']
