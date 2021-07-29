from django import forms

from ekabis.models.ConnectionCapacity import ConnectionCapacity

CHOICES_WITH_BLANK = (
    ('', '-------'),

)


class ConnectionCapacityForm(forms.ModelForm):
    class Meta:
        model = ConnectionCapacity
        fields = ('name', 'value', 'unit', 'city', 'district')

        labels = {'name': 'Bağlantı Kapasitesi *', 'value': 'Miktar *', 'unit': 'Birim *','city':'Şehir *','district':'İlçe *'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'value': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', "onChange": 'ilceGetir()', }),
            'district': forms.Select(choices=CHOICES_WITH_BLANK,
                                     attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id',
                                            }),

        }
