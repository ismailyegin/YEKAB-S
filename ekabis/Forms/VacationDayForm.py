from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.VacationDay import VacationDay


class VacationDayForm(BaseForm):
    class Meta:
        model = VacationDay
        fields = ('definition', 'date')
        labels = {'definition': 'Açıklama', 'date': 'Tatil Tarihi'}
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "mm/dd/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }
