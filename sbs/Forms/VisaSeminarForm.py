from django import forms
from django.forms import ModelForm
from sbs.models.VisaSeminar import VisaSeminar
class VisaSeminarForm(ModelForm):
    class Meta:
        model = VisaSeminar
        fields = (
            'name', 'startDate', 'finishDate', 'location', 'branch',
            'application', 'appStartDate', 'appFinishDate','year'
        )
        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'location': 'Yer', 'branch': 'Branş',
                  'application': 'Online Basvuru açık mı?', 'appStartDate': 'Online Basvuru Başlangıc Tarihi',
                  'appFinishDate': 'Online Basvuru Bitiş tarihi','year':'Geçerlilik Yılı'
                  }
        widgets = {
            'application': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%; '}),
            'appStartDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'on',
                       }),
            'year': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'appFinishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker3', 'autocomplete': 'on',
                       }),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'on',
                       }),
            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'on',
                       }),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}),

            'location': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}),

        }
