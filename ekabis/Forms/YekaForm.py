from django import forms

from ekabis.models import Company, Person, Employee
from ekabis.models.Yeka import Yeka


class YekaForm(forms.ModelForm):
    class Meta:
        model = Yeka

        fields = ('date', 'definition', )


        labels = {'definition': 'Tanım '}
        widgets = {
            'definition': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),


        }

