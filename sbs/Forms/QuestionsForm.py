from django import forms
from django.forms import ModelForm

from sbs.models.Question import Question


class QuestionsForm(ModelForm):
    class Meta:
        model = Question

        fields = (
            'question', 'reaply', 'count', 'isActiv')
        labels = {'question': 'Sorunuzu Giriniz:', 'reaply': 'Cevabı giriniz', 'count': 'Sırasi',
                  'isActiv': 'Aktiv mi? '}

        widgets = {

            'question': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"}),

            'reaply': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

        }
