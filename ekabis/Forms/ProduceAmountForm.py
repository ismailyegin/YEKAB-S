from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ProduceAmount import ProduceAmount


class ProduceAmountForm(BaseForm):
    class Meta:
        model = ProduceAmount
        fields = ('quantity', 'date',)
        labels = {'quantity': 'Miktar(GWh)',
                  'date': 'Tarih',

                  }
        widgets = {

            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "mm/dd/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control ', 'required': 'required'}),

        }
