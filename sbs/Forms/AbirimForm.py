from django import forms
from django.forms import ModelForm

from sbs.models.Abirim import Abirim


class AbirimForm(ModelForm):
    class Meta:
        model = Abirim
        fields = ('name',)
    def __init__(self, *args, **kwargs):
        super(AbirimForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




