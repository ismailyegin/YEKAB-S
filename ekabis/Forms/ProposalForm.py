from django import forms
from ekabis.Forms.BaseForm import BaseForm

from ekabis.models.Proposal import Proposal
class ProposalForm(BaseForm):
    class Meta:
        model = Proposal
        fields = ('farm_form', 'kml_file','information_form','name','date','capacity','order',)
        labels = {'farm_form': 'Tarım Yazısı',
                  'information_form': 'Bilgi Formu',
                  'date': 'Başvuru Tarihi*',
                  'capacity': 'Kapasite*',
                  'name':'Aday Yeka Adı*',
                  'order':'Sıralama'
                  }
        widgets = {
            'date':forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'capacity':forms.NumberInput(
                attrs={'class': 'form-control ','required': 'required'}),
            'order': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }