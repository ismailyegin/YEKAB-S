from django import forms
from django.forms import ModelForm

from sbs.models.Adosya import Adosya


class AdosyaFormSearch(ModelForm):
    class Meta:
        model = Adosya
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(AdosyaFormSearch,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = False