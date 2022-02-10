from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ExtraTime import ExtraTime

CHOICES = (('is_gunu', 'İş Günü'), ('takvim_gunu', 'Takvim Günü'),)


class ExtraTimeForm(BaseForm):
    class Meta:
        model = ExtraTime
        fields = ('definition','added_date', 'time', 'time_type',  'file')
        labels = {'time': 'Ek Süre', 'time_type': 'Süre Türü', 'definition': 'Konu',
                  'added_date': 'Ek Süre Başlama Tarihi', 'file': 'Ek Süre Belgesi'}
        widgets = {
            'time': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'definition': forms.TextInput(
                attrs={'class': 'form-control '}),
            'time_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                              'style': 'width: 100%; ', }),
            'added_date': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'required': 'required', 'id': 'datepicker4',
                       'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
        }
