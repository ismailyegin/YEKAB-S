from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import YekaCompetition, City
from ekabis.models.YekaCompetition import YekaCompetition


class YekaCompetitionForm(BaseForm):

    class Meta:
        model = YekaCompetition
        fields = ('name', 'capacity',)
        labels = {'name': 'Tanımı *',
                  'date':'Resmi Gazetede Yayın Tarihi *','capacity':'Kapasite (MWe) *'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),
            # 'date': forms.DateInput(
            #     attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
            #            'onkeydown': 'return false', 'required': 'required'}),


        }


