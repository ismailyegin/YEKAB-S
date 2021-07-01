from django import forms
from django.forms import ModelForm

from ekabis.models.Person import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage', 'birthDate', 'gender', 'birthplace', 'bloodType')
        labels = {'tc': 'T.C.', 'gender': 'Cinsiyet', 'profileImage': 'Profil Resmi'}

        widgets = {
            'profileImage': forms.FileInput(),

            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'maxlength': '11', 'minlength': '11',
                       'onkeypress': 'validate(event)', 'name': 'tc', 'id': 'tc'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'required': 'required'}),
            'birthplace': forms.TextInput(
                attrs={'class': 'form-control '}),
            'bloodType': forms.TextInput(
                attrs={'class': 'form-control '}),

        }
