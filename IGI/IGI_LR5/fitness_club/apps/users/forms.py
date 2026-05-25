import re
from datetime import date

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.users.models import Client


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя или email',
        widget=forms.TextInput(attrs={
            'placeholder': 'username или email'
        }),
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        }),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    full_name = forms.CharField(
        max_length=200,
        label='ФИО'
    )

    date_of_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Только для лиц старше 18 лет'
    )

    phone = forms.CharField(
        max_length=25,
        label='Телефон',
        help_text='Формат: +375 (29) XXX-XX-XX'
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label='Адрес'
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'full_name',
            'date_of_birth',
            'phone',
            'address',
            'password1',
            'password2',
        )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Имя пользователя уже занято')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email уже используется')

        return email

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']

        today = date.today()

        age = (
            today.year
            - dob.year
            - ((today.month, today.day) < (dob.month, dob.day))
        )

        if age < 18:
            raise ValidationError(
                f'❌ Вам {age} лет. Регистрация разрешена только с 18 лет!'
            )

        return dob

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        pattern = r'^\+375\s?\(?(29|25|33|44)\)?\s?[0-9]{3}[-\s]?[0-9]{2}[-\s]?[0-9]{2}$'

        if not re.match(pattern, phone):
            raise ValidationError(
                'Неверный формат телефона. Пример: +375 (29) 123-45-67'
            )

        return phone

    def save(self, commit=True):
        full_name = self.cleaned_data['full_name'].strip()

        parts = full_name.split()

        first_name = parts[0] if parts else ''

        last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = first_name
        user.last_name = last_name

        if commit:
            user.save()

            client = Client.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
            )

            return user, client

        return user


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client

        fields = [
            'date_of_birth',
            'phone',
            'address'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']

        today = date.today()

        age = (
            today.year
            - dob.year
            - ((today.month, today.day) < (dob.month, dob.day))
        )

        if age < 18:
            raise ValidationError(
                f'❌ Вам {age} лет. Возраст должен быть не менее 18 лет!'
            )

        return dob