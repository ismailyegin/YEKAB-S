

from django import forms
from django.forms import ModelForm

from ekabis.models.CompanyFileNames import CompanyFileNames
class CompanyFileNameForm(ModelForm):
    class Meta:
        model = CompanyFileNames
        fields = (
            'name',
            'is_active',

        )
        labels = {'name': 'Dokuam- İsmi',
                  'is_active': 'Ön kayıtta olsun mu ?',

                  }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'is_active':forms.BooleanField(attr={'class': 'form-control ', 'required': 'required'})
        }