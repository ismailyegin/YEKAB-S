from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class DisabledUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')
        labels = {'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email'}
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'readonly': 'readonly', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required', 'readonly': 'readonly'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper', 'readonly': 'readonly'}),

        }
