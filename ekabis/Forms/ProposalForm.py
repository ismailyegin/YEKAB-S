from django import forms
from ekabis.Forms.BaseForm import BaseForm

from ekabis.models.Proposal import Proposal
class ProposalForm(BaseForm):
    class Meta:
        model = Proposal
        fields = ('farm_form', 'information_form','name','date','capacity')
        labels = {'farm_form': 'Tarım Yazısı',
                  'information_form': 'Bİlgi Formu',
                  'date': 'Başvuru Tarihi',
                  'capacity': 'Kapasite',
                  'name':'İsim',
                  }
        widgets = {
            'farm_form': forms.FileInput(attrs={'class': '',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'date':forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'information_form': forms.FileInput(attrs={'class': '',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'capacity':forms.NumberInput(
                attrs={'class': 'form-control ','required': 'required'}),
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }