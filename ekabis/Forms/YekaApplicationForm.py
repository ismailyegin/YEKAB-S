from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaApplication import YekaApplication


class YekaApplicationForm(forms.ModelForm):
    class Meta:
        model = YekaApplication
        fields = ('startDate', 'finishDate','preRegistration',)
        labels = {'startDate': 'Basvuru Başlangıç Tarihi',
                  'finishDate': 'Basvuru Bitiş Tarihi',
                  'preRegistration': 'Basvuru Aç'}
        widgets = {
            'preRegistration': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

        }
