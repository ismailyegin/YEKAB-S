from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ConnectionUnit import ConnectionUnit


class ConnectionUnitForm(BaseForm):
    class Meta:
        model = ConnectionUnit
        fields = ('name',)

        labels = {'name': 'Birim '}
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
         }
