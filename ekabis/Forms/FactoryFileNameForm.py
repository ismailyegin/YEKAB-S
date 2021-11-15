from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.FactoryFileName import FactoryFileName


class FactoryFileNameForm(BaseForm):
    class Meta:
        model = FactoryFileName
        fields = ('name',)
        labels = {'name': 'Doküman İsmi', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
