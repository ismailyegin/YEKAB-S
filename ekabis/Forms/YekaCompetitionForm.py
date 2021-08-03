from django import forms

from ekabis.models import YekaCompetition, City
from ekabis.models.YekaCompetition import YekaCompetition


class YekaCompetitionForm(forms.ModelForm):

    class Meta:
        model = YekaCompetition
        fields = ('name', 'capacity','date')
        labels = {'name': 'Tanımı',
                  'date':'Resmi Gazetede Yayın Tarihi'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),


        }


