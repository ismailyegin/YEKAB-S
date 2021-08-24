from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from captcha.fields import CaptchaField


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'id': 'username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'type': 'password', 'id': 'password'}))


class CaptchaForm(forms.Form):
    captcha = CaptchaField()
