from django import forms
from django.forms import ModelForm

from sbs.models import Person


class DisabledPersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage', 'height', 'weight', 'birthDate', 'bloodType', 'gender', 'birthplace', 'motherName',
            'fatherName')
        labels = {'tc': 'T.C.', 'gender': 'Cinsiyet'}

        widgets = {

            'tc': forms.TextInput(attrs={'class': 'form-control ', 'readonly': 'readonly'}),

            'height': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'weight': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'readonly': 'readonly'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'readonly': 'readonly'}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'readonly': 'readonly'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                        'readonly': 'readonly'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; ', 'disabled': 'disabled'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'disabled': 'disabled'}),

        }
