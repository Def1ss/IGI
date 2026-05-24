from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from apps.users.models import Client


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя или email',
        widget=forms.TextInput(attrs={'placeholder': 'username или email'}),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='Логин')
    email = forms.EmailField(label='Email')
    full_name = forms.CharField(max_length=200, label='ФИО')
    date_of_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    phone = forms.CharField(max_length=25, label='Телефон')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), label='Адрес')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Имя пользователя уже занято')
        return username

    def save(self):
        full_name = self.cleaned_data['full_name'].strip()
        parts = full_name.split()
        first_name = parts[0] if parts else ''
        last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password='strength_client_pass',
            first_name=first_name,
            last_name=last_name,
        )
        client = Client.objects.create(
            user=user,
            date_of_birth=self.cleaned_data['date_of_birth'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address'],
        )
        return user, client


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['date_of_birth', 'phone', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
