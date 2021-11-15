from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Factory import Factory


class FactoryForm(BaseForm):
    class Meta:
        model = Factory
        fields = ('name', 'date',)
        labels = {'date': 'Kuruluş Tarihi', 'name': 'Fabrika İsmi', }
        widgets = {
            'date':forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
