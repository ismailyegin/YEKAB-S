from django import forms
from django.forms import ModelForm

from sbs.models.Aklasor import Aklasor
from sbs.models.CategoryItem import CategoryItem


class AklasorSearchForm(ModelForm):
    class Meta:
        model = Aklasor
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(AklasorSearchForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.required = False

        self.fields['location'].queryset=CategoryItem.objects.filter(forWhichClazz="location")
        self.fields['startyear'].widget.attrs['class'] = 'form-control  dateyear'
        self.fields['finishyear'].widget.attrs['class'] = 'form-control  dateyear'


