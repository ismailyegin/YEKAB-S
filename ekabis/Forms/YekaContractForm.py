from django import forms
from django.forms import ModelForm
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaContract import YekaContract
class YekaContractForm(BaseForm):
    class Meta:
        model = YekaContract
        fields = ('price', 'contract','date','unit','company')
        labels = {
                  'price': 'Fiyat',
                  'contract': 'Kullanım Hakkı Sözleşmesi',
                  'date': 'Sözleşme İmza Tarihi',
                  'unit': 'Bİrimi',
                  'contract': 'Kullanım Hakkı Sözleşmesi',
                  'company': 'Kazanan Firma',}
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control ','required': 'required'}),
            'company':forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            # 'contract':forms.FileInput(attrs={'class': 'files',
            #                             'style': 'width: 100%;', 'required': 'required'}),
        }
