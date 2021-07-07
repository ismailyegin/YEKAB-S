from django import forms
from django.forms import ModelForm

from ekabis.models.Company import Company
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = (
            'name',
            'degree',
            'taxOffice',
            'taxnumber',
            'mail',
        )
        labels = {'name': 'Firma İsmi',
                  'degree': 'Unvan',
                  'taxOffice': 'Vergi Dairesi',
                  'taxnumber': 'Vergi Numarası',
                  'mail': 'Mail Adresi ',
                  }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'degree': forms.TextInput(attrs={'class': 'form-control '}),
            'taxOffice': forms.TextInput(attrs={'class': 'form-control '}),
            'taxnumber': forms.TextInput(attrs={'class': 'form-control ','onkeypress': 'validate(event)'}),
            #'taxnumber': forms.TextInput(attrs={'class': 'form-control ','pattern':'^\$\d{1.}(.\d{3})*(\,\d+)?$','data-type':'currency'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control '}),
        }
