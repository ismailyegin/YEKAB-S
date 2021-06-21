from django import forms
from django.forms import ModelForm

from ekabis.models.CategoryItem import CategoryItem
from ekabis.models.Company import Company


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = (

            'name',
            'sorumlu',
            'isFormal',
            'degree',
            'taxOffice',
            'taxnumber',
            'mail',

        )
        labels = {'name': 'Firma İsmi',
                  'sorumlu ': 'Firma  Sorumlusu',
                  'isFormal': 'Firma  Türü ',
                  'degree': 'Unvan',
                  'taxOffice': 'Verdi Dairesi',
                  'taxnumber': 'Vergi Numarası',
                  'mail': 'Mail Adresi ',

                  }
        widgets = {

            'isFormal': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%; '}),

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'sorumlu': forms.TextInput(attrs={'class': 'form-control '}),
            'degree': forms.TextInput(attrs={'class': 'form-control '}),
            'taxOffice': forms.TextInput(attrs={'class': 'form-control '}),
            'taxnumber': forms.TextInput(attrs={'class': 'form-control '}),
            # 'taxnumber': forms.TextInput(attrs={'class': 'form-control ','pattern':'^\$\d{1.}(.\d{3})*(\,\d+)?$','data-type':'currency'}),
            'mail': forms.TextInput(attrs={'class': 'form-control '}),

        }
