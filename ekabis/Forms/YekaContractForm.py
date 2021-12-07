from django import forms
from django.forms import ModelForm
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaContract import YekaContract


class YekaContractForm(BaseForm):
    class Meta:
        model = YekaContract

        fields = ('price', 'unit', 'company', 'contract','eskalasyonMaxPrice',)
        labels = {
            'price': 'Fiyat',
            'eskalasyonMaxPrice':'Eskalasyon Tavan Fiyatı',
            'contract': 'Kullanım Hakkı Sözleşmesi',
            'unit': 'Birimi',
            'company': 'Kazanan Firma', }
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible', 'disabled': 'disabled',
                                           'style': 'width: 100%;'}),
            # 'contract_date': forms.DateInput(
            #     attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
            #            'onkeydown': 'return false', 'required': 'required'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'eskalasyonMaxPrice': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'company': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;'}),
            # 'contract':forms.FileInput(attrs={'class': 'files',
            #                             'style': 'width: 100%;', 'required': 'required'}),
        }


