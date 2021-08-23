
from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaCompany import YekaCompany

class YekaCompanyForm(BaseForm):
    class Meta:
        model = YekaCompany
        fields = ('company','price' )

        labels = {'company': 'Firma ',
                  'price':'Fiyat'}
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'price':forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }