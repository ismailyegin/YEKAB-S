from django import forms
from django.forms import ModelForm

from ekabis.models.YekaApplicationFile import YekaApplicationFile


class YekaApplicationFileForm(ModelForm):
    class Meta:
        model = YekaApplicationFile
        fields = ('file',)
        labels = {'file': 'Dosya',}

