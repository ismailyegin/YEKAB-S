from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.CompetitionCompany import CompetitionCompany
from ekabis.models.YekaApplication import YekaApplication
class CompetitionCompanyForm(BaseForm):

    class Meta:
        model = CompetitionCompany
        fields = (
            'price',
            'company',
        )
        labels = {'price': 'Fiyat',
                  'company':'Firma'
                  }
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'price': forms.NumberInput(
                attrs={'class': 'form-control ','required': 'required'}),
        }
