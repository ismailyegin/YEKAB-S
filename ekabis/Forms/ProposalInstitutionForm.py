from django import forms
from ekabis.Forms.BaseForm import BaseForm

from ekabis.models.Proposalnstitution import ProposalInstitution

Choices = (
    ('Sonuçlanmadı', 'Sonuçlanmadı'),
    ('Olumlu', 'Olumlu'),
    ('Olumsuz', 'Olumsuz'),

)


class ProposalInstitutionForm(BaseForm):
    class Meta:
        model = ProposalInstitution
        fields = ('status','number', 'date', 'file',)
        labels = {'status': 'Onay Durumu','number': 'Sayı',
                  'file': 'Dosya',
                  'date': 'Tarih',

                  }
        widgets = {

            'status': forms.Select(choices=Choices, attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                           'style': 'width: 100%;', 'required': 'required'}),
            'number': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'style': "margin-bottom: 10px",
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),


        }
