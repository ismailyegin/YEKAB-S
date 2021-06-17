from django import forms
from django.forms import ModelForm

from sbs.models.Level import Level



class VisaForm(ModelForm):
    class Meta:
        model = Level

        fields = (
            'dekont', 'branch', 'startDate')

        labels = {'branch': 'Branş', 'startDate': 'Geçerlilik yılı'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker5', 'autocomplete': 'off',
                       }),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
