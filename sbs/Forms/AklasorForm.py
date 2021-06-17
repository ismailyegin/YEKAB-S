from django import forms
from django.forms import ModelForm

from sbs.models.Aklasor import Aklasor
from sbs.models.CategoryItem import CategoryItem


class AklasorForm(ModelForm):
    class Meta:
        model = Aklasor
        fields = ['name','sirano','location','birim','startyear','finishyear']
    def __init__(self, *args, **kwargs):
        super(AklasorForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['finishyear'].widget.attrs['class'] = 'form-control dateyear'
        self.fields['startyear'].widget.attrs['class'] = 'form-control dateyear'
        self.fields['location'].queryset=CategoryItem.objects.filter(forWhichClazz="location")




