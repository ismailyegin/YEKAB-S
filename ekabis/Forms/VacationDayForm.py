from django import forms
from django.forms import ModelForm

from ekabis.models.VacationDay import VacationDay


class VacationDayForm(ModelForm):
    class Meta:
        model = VacationDay
        fields = ('definition', 'date')
        labels = {'definition': 'Açıklama', 'date': 'Tatil Tarihi'}
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

        }
