from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaUser import YekaUser
from ekabis.models.Employee import Employee


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
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'finisDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'file':forms.FileInput(attrs={'class': '',
                                        'style': 'width: 100%;', 'required': 'required'}),
        }


