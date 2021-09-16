from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaApplicationFileName import YekaApplicationFileName


class YekaApplicationFileNameForm(BaseForm):
    class Meta:
        model = YekaApplicationFileName
        fields = ('filename',)
        labels = {'filename': 'İsim',}
        widgets = {
            'filename': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required'}),

        }
