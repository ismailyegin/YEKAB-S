from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Employment import Employment



class EmploymentForm(BaseForm):
    class Meta:
        model = Employment
        fields = ('employmentFile','employmentDate',)
        labels = {'employmentDate': 'Tarih',
                  'employmentFile': 'İstihdam Dokümanı',
                  }
        widgets = {

            'employmentDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }