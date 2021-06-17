from django import forms
from django.forms import ModelForm

from sbs.models.Activity import Activity


class ActivityForm(ModelForm):
    class Meta:
        model = Activity

        fields = (
            'name', 'startDate', 'finishDate', 'eventPlace', 'type', 'year')

        labels = {'name': 'Tanımı', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'eventPlace': 'Etkinlik Yeri', 'type': 'Faaliyet Türü ', 'year': 'Yılı ', }

        widgets = {

            'year': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker5', 'autocomplete': 'on',
                       }),

            'eventPlace': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'on',
                       }),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'on',
                       }),

            'name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}),

            'type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; '}),

        }
