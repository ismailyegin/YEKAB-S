from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import ConnectionRegion, City
class ConnectionRegionForm(BaseForm):
    cities = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = ConnectionRegion
        fields = ('name', 'capacity',)

        labels = {'name': 'Bağlantı Bölgesi *','capacity':'Kapasite (MWe) *'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cities'].queryset = City.objects.filter(isDeleted=False)
        self.fields['cities'].label = 'Şehirler *'
        self.fields['cities'].widget.attrs = {'class': 'form-control select2 select2-hidden-accessible',
                                                        'style': 'width: 100%;', 'data-select2-id': '7',
                                                        'data-placeholder': 'Bağlanti Bölgesi Seçiniz', }
