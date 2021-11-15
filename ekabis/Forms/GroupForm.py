from django import forms
from django.contrib.auth.models import Group

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Permission import Permission


class GroupForm(BaseForm):
    class Meta:
        model = Group
        fields = ('name',)
        labels = {'name': 'İsim '}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
        }