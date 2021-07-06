from django import forms

from ekabis.models.ConnectionUnit import ConnectionUnit


class ConnectionUnitForm(forms.ModelForm):
    class Meta:
        model = ConnectionUnit
        fields = ('name',)

        labels = {'name': 'Birim '}
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
         }
