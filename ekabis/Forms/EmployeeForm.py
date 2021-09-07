from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Employee import Employee


class EmployeeForm(BaseForm):
    class Meta:
        model = Employee

        fields = ()
        labels = {}


