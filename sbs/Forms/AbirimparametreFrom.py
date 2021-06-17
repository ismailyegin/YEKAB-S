from django import forms
from django.forms import ModelForm

from sbs.models.AbirimParametre import AbirimParametre

class AbirimparametreForm(ModelForm):
    class Meta:
        model = AbirimParametre
        fields =('type','title')
    def __init__(self, *args, **kwargs):
        super(AbirimparametreForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'