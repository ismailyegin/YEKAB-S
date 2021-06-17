from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserSearchForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active',)
        labels = {'first_name': 'İsim', 'last_name': 'Soyisim'}
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Ad', 'value': '',
                       "style": "text-transform:uppercase"}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyad', "style": "text-transform:uppercase"}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Şifre',}),

        }
