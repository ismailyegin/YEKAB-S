from django import forms
from django.forms import ModelForm

from ekabis.models.Employee import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee

        fields = (
            'workDefinition',)
        labels = {'workDefinition': 'İş Tanımı'}


