
from django import forms
from ekabis.models.ExtraTimeFile import ExtraTimeFile

class ExtraTimeFileForm(forms.ModelForm):
    class Meta:
        model = ExtraTimeFile
        fields = ('definition','file')
        labels = {'definition': 'Açıklama '}
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control ',}),
        }