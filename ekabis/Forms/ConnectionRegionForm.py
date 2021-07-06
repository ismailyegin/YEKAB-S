from django import forms

from ekabis.models import ConnectionRegion


class ConnectionRegionForm(forms.ModelForm):
    class Meta:
        model = ConnectionRegion
        fields = ('name', 'value', 'unit')

        labels = {'name': 'Bağlantı Bölgesi '}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'value': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'required': 'required'}),

        }
