from django import forms
from django.forms import ModelForm

from sbs.models.Document import Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = (
            'file', 'name',)
        labels = {'file ': 'Dosya Seçiniz', 'name ': 'Döküman İsmi', }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}),
        }
