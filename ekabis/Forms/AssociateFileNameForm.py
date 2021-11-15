from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.AssociateDegreeFileName import AssociateDegreeFileName


class AssociateFileNameForm(BaseForm):
    class Meta:
        model = AssociateDegreeFileName
        fields = ('name',)
        labels = {'name': 'Doküman İsmi', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
