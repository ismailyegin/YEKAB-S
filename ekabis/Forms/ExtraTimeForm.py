from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ExtraTime import ExtraTime

CHOICES = (('is_gunu', 'İş Günü'), ('takvim_gunu', 'Takvim Günü'),)


class ExtraTimeForm(BaseForm):
    class Meta:
        model = ExtraTime
        fields = ('definition','time', 'time_type',)
        labels = {'time': 'Ek Süre', 'time_type': 'Süre Türü','definition':'Konu'}
        widgets = {
            'time': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'definition': forms.TextInput(
                attrs={'class': 'form-control '}),
            'time_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                              'style': 'width: 100%; ', }),
        }
