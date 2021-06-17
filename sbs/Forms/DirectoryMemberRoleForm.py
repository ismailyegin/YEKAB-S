from django import forms
from django.forms import ModelForm

from sbs.models import DirectoryMemberRole


class DirectoryMemberRoleForm(ModelForm):
    class Meta:
        model = DirectoryMemberRole
        fields = ('name',)
        labels = {'name': 'Kurul Üye Rol Adı'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"})
        }
