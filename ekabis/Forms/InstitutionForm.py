from django import forms
from ekabis.models.Institution import Institution
from ekabis.Forms.BaseForm import BaseForm

class InstitutionForm(BaseForm):
    class Meta:
        model = Institution
        fields = ('name',)
        labels = {
            'name': 'Kurum İsmi',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ',}),



        }
