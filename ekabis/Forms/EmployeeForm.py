from django import forms
from django.forms import ModelForm

from ekabis.models.Employee import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee

        fields = (
            'workDefinition',)
        labels = {'workDefinition': 'İş Tanımı'}

        widgets = {

            'workDefinition': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),


        }
