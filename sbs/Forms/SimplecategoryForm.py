from django import forms
from django.forms import ModelForm
from sbs.models.SimpleCategory import SimpleCategory


class SimplecategoryForm(ModelForm):
    class Meta:
        model = SimpleCategory

        fields = ('categoryName',)

        labels = {'categoryName': 'İsim'}

        widgets = {

            'categoryName': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

        }
