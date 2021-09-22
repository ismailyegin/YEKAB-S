

from django import forms
from ekabis.Forms.BaseForm import BaseForm

from ekabis.models.Proposalnstitution import ProposalInstitution
class ProposalInstitutionForm(BaseForm):
    class Meta:
        model = ProposalInstitution
        fields = ('status', 'date','file')
        labels = {'status': 'Onay Durumu',
                  'file': 'Dosya',
                  'date':'Tarih',

                  }
        widgets = {

            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', 'required': 'required', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }