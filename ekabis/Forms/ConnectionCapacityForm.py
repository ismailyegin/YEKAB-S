from django import forms

from ekabis.models.ConnectionCapacity import ConnectionCapacity


class ConnectionCapacityForm(forms.ModelForm):
    class Meta:
        model = ConnectionCapacity
        fields = ('name', 'value', 'unit')

        labels = {'name': 'Bağlantı Kapasitesi '}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'value': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'required': 'required'}),

        }
