from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.CalendarName import CalendarName


class CalendarNameForm(BaseForm):
    class Meta:
        model = CalendarName
        fields = ('name','color')
        labels = {'name': 'Tanımı', 'color':'Renk Seçiniz'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'color': forms.TextInput(
                attrs={'class': 'input-group my-colorpicker2 colorpicker-element ', 'required': 'required'}),

        }

