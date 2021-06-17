from django import forms
from django.forms import ModelForm

from sbs.models.Deposit import Deposit


class DepositForm(ModelForm):
    class Meta:
        model = Deposit

        fields = (
            'date',
            'description',
            'count',
            'delivery',
            'club',
            'product',
        )
        labels = {
            'date': 'Tarih',
            'description': 'Açıklama',
            'count': 'Miktar',
            'delivery': 'Teslim Alan',
            'club': 'Klüp',
            'product': 'Malzeme',
        }

        widgets = {

            'club': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),
            'product': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; ', 'required': 'required'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                        'required': 'required'}),

            'description': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'delivery': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'count': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

        }
