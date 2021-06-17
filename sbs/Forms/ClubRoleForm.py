from django import forms
from django.forms import ModelForm

from sbs.models import ClubRole


class ClubRoleForm(ModelForm):
    class Meta:
        model = ClubRole
        fields = ('name',)
        labels = {'name': 'Kulüp Üye Rol Adı'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"})
        }
