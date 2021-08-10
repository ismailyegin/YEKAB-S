from django import forms
from django.forms import ModelForm

from ekabis.models.Communication import Communication
from ekabis.models.Country import Country


class CommunicationForm(ModelForm):

    class Meta:
        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'country', 'city', 'phoneHome', 'phoneJop',
            'addressHome', 'addressJop')
        labels = {'phoneNumber': 'Cep Telefonu',
                  'phoneNumber2': 'Sabit Telefon',
                  'phoneHome': 'Ev Telefonu',
                  'phoneJop': 'İş Telefonu',
                  'addressHome': 'Ev Adresi',
                  'addressJop': 'İş Adresi',
                  'postalCode': 'Posta Kodu',
                  'city': 'İl', }
        widgets = {

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),


        }
