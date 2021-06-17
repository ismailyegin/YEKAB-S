from django import forms
from django.forms import ModelForm
class AevrakForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'accept':'application/pdf',}))








