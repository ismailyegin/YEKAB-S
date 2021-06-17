from django import forms
from django.forms import ModelForm

from sbs.models.Abirim import Abirim


class AbirimSearchForm(ModelForm):
    class Meta:
        model = Abirim
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(AbirimSearchForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = False




