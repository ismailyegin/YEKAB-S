from django import forms
from django.forms import ModelForm

from sbs.models.Employe import Employe


class EmployeUnitForm(ModelForm):
    class Meta:
        model = Employe
        fields = (
             'birim',)
        labels = {'birim ': 'Birim', }
        widgets = {

            'birim': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;', 'required': 'required'}),

        }
