from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Competition import Competition



class CompanyUserForm(BaseForm):

    class Meta:
        model = Competition
        fields = (
            'date',
            'report',

        )
        labels = {'report': 'Yarışma Tutanağı',
                  'date': 'Yarışma Zamanı',
                  }
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                       'readonly': 'readonly'}),
        }
