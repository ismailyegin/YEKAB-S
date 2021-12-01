from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import Accept


class AcceptForm(BaseForm):
    class Meta:
        model = Accept
        fields = ('date',  'currentPower', 'installedPower','report')
        labels = {'date': 'Kabul Tarihi', 'report': 'Kabul Tutanağı',
                  'installedPower': 'İşletmedeki Mekanik Güç  (MWm)',
                  'currentPower': 'İşletmedeki Elektiriksel Güç  (MWe)'}
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'currentPower': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'installedPower': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
