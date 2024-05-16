from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, EmailInput, EmailField, PasswordInput, forms
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

User = get_user_model()


class RegisterForm(UserCreationForm):
    username = CharField(max_length=32, min_length=3, required=True, widget=TextInput(attrs={"class": "form-control"}))
    email = EmailField(max_length=64, required=True, widget=EmailInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(max_length=13, min_length=13, required=True,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': '+380XXXXXXXXX', "class": "form-control"}))
    telegram_nickname = forms.CharField(max_length=32, required=False,
                                        widget=forms.TextInput(
                                            attrs={'placeholder': '@nickname', "class": "form-control"}))
    password1 = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))
    password2 = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'telegram_nickname', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This e-mail address is already in use.')
        return email

    def clean_telegram_nickname(self):
        telegram_nickname = self.cleaned_data.get('telegram_nickname')
        if telegram_nickname:
            if not telegram_nickname.startswith('@'):
                telegram_nickname = '@' + telegram_nickname
            if User.objects.filter(telegram_nickname=telegram_nickname).exists():
                self.add_error('telegram_nickname',
                               ValidationError(gettext_lazy('This telegram nickname is already in use.'),
                                               code='invalid'))
        return telegram_nickname


class LoginForm(AuthenticationForm):
    username = CharField(max_length=32, min_length=3, required=True, widget=TextInput(attrs={"class": "form-control"}))
    password = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
