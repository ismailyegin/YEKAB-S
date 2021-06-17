from django import forms
from django.forms import ModelForm

from sbs.models.Judge import Judge


class IbanFormJudge(ModelForm):
    class Meta:
        model = Judge

        fields = (
            'iban',)
        labels = {'iban': 'İban Adresi:', }
        widgets = {

            'iban': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', }),
        }
