from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import Guarantee

from ekabis.models.Proposal import Proposal
STATUS_CHOICES = (
    (("İrat"), ("İrat")),
    (("İade"), ("İade")),
    (("Muhafaza"), ("Muhafaza")),


)

class GuaranteeForm(BaseForm):
    class Meta:
        model = Guarantee
        fields = ('guaranteeFile','rebateDate','bank','branch','reference','pikur', 'quantity','guaranteeTime','guaranteeCount','guaranteeDate','status','definition',)
        labels = {'bank': 'Banka',
                  'branch': 'Şube',
                  'guaranteeDate': 'Teminat Tarihi',
                  'guaranteeCount': 'Teminat Sayısı',
                  'guaranteeTime':'Teminat Süresi',
                  'status':'Teminat Durumu',
                  'definition':'Açıklama',
                  'guaranteeFile':'Teminat Mektubu',
                  'quantity':'Tutar',
                  'pikur':'Pikur',
                  'reference':'Referans','rabateDate':'İade Tarihi'
                  }
        widgets = {


            'guaranteeCount':forms.NumberInput(
                attrs={'class': 'form-control '}),
            'guaranteeTime': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control '}),
            'bank': forms.TextInput(attrs={'class': 'form-control ', }),
            'branch': forms.TextInput(attrs={'class': 'form-control '}),
            'reference': forms.TextInput(attrs={'class': 'form-control '}),
            'pikur': forms.TextInput(attrs={'class': 'form-control ' }),
            'definition': forms.TextInput(attrs={'class': 'form-control '}),
            'status': forms.Select(choices=STATUS_CHOICES,
                                 attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),
            'guaranteeDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'rebateDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }