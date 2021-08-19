from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Competition import Competition


class CompanyUserForm(BaseForm):
    class Meta:
        model = Competition
        fields = (
            'report',
            'date',
        )
        labels = {'report': 'Yarışma Tutanağı',
                  'date': 'Yarışma Zamanı',
                  }
        widgets = {
            'report': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                       'readonly': 'readonly'}),
        }
