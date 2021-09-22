from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaUser import YekaUser


class YekaUserForm(BaseForm):
    class Meta:
        model = YekaUser
        fields = ('user','startDate','finisDate','file')
        labels = {
                  'user': 'Firma Kullanıcısı',
                  'startDate': 'Yetki Başlangıç Tarihi',
                  'finisDate': 'Yetki Bitiş Tarihi',
                  'file': 'Atama Yazısı',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

            'finisDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'id': 'datepicker2', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            #
            # 'file': forms.FileInput(attrs={'class': '',
            #                                'style': 'width: 100%;', 'required': 'required'}),
        }


