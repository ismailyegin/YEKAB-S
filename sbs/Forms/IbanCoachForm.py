from django import forms
from django.forms import ModelForm

from sbs.models.Coach import Coach


class IbanCoachForm(ModelForm):
    class Meta:
        model = Coach

        fields = (
            'iban',)
        labels = {'iban': 'İban Adresi:', }
        widgets = {

            'iban': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', }),
        }
