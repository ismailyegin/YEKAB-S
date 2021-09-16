from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaApplicationFile import YekaApplicationFile


class YekaApplicationFileForm(BaseForm):
    class Meta:
        model = YekaApplicationFile
        fields = ('file',)
        labels = {'file': 'Dosya',}

