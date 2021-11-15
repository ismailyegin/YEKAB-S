
from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ExtraTimeFile import ExtraTimeFile

class ExtraTimeFileForm(BaseForm):
    class Meta:
        model = ExtraTimeFile
        fields = ('definition','file')
        labels = {'definition': 'Açıklama '}
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control ',}),
        }