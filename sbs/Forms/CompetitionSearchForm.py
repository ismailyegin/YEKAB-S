from django import forms
from django.forms import ModelForm

from sbs.models import Competition


class CompetitionSearchForm(ModelForm):
    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate',)

        labels = {'name': 'İsim', 'startDate': 'Başlangıç Yılı', 'finishDate': 'Yılı ', }

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker5', 'autocomplete': 'on',
                       }),

            'name': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

        }
