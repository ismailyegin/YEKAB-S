from django import forms
from django.forms import ModelForm

from sbs.models.Penal import Penal


class PenalForm(ModelForm):
    class Meta:
        model = Penal
        fields = ('file',
                  'penal',)
        labels = {'file': 'Döküman', 'penal': 'Ceza İsmi ', }
        widgets = {'penal': forms.TextInput(
            attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}), }
