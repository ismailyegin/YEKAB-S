from django import forms
from django.forms import ModelForm
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaContract import YekaContract


class YekaContractForm(BaseForm):
    class Meta:
        model = YekaContract
        fields = ('price', 'unit', 'contractDate', 'company', 'contract',)
        labels = {
            'price': 'Fiyat',
            'contract': 'Kullanım Hakkı Sözleşmesi',
            'contractDate': 'Sözleşme İmza Tarihi',
            'unit': 'Birimi',
            'company': 'Kazanan Firma', }
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),
            'contractDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'company': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;'}),
            # 'contract':forms.FileInput(attrs={'class': 'files',
            #                             'style': 'width: 100%;', 'required': 'required'}),
        }
