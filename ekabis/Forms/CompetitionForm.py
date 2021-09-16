from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Competition import Competition



class CompetitionForm(BaseForm):

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
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "mm/dd/yyyy", "data-mask": "", "inputmode": "numeric"}),
        }
