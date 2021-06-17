from django import forms
from django.forms import ModelForm
from sbs.models.VisaSeminar import VisaSeminar


class VisaSeminarSearchForm(ModelForm):
    class Meta:
        model = VisaSeminar
        fields = (
            'name', 'startDate', 'finishDate', 'location')
        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'location': 'Yer', }
        widgets = {
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'on',
                       }),
            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'on',
                       }),

            'name': forms.TextInput(
                attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'location': forms.TextInput(
                attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

        }

    def __init__(self, *args, **kwargs):
        super(VisaSeminarSearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['location'].required = False
        self.fields['finishDate'].required = False
        self.fields['startDate'].required = False
