from django import forms
from django.forms import ModelForm

from sbs.models import Communication


class DisabledCommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city', 'country')
        labels = {'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke'}
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', 'readonly': 'readonly'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control ', 'readonly': 'readonly'}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control ', 'readonly': 'readonly'}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control ', 'readonly': 'readonly'}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required', 'disabled': 'disabled'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required', 'disabled': 'disabled'}),

        }
