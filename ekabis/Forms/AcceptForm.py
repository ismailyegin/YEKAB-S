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
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'currentPower': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required' ,'placeholder':'Tam sayı olmayan değerler için . kullanın'}),
            'installedPower': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required' ,'placeholder':'Tam sayı olmayan değerler için . kullanın'}),

        }
