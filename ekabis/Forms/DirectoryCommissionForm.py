from django import forms
from django.forms import ModelForm

from ekabis.models.DirectoryCommission import DirectoryCommission


class DirectoryCommissionForm(ModelForm):
    class Meta:
        model = DirectoryCommission
        fields = ('name',)
        labels = {'name': 'Kurul Adı'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"})
        }
