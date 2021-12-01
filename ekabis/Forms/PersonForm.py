from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Person import Person


class PersonForm(BaseForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage', )
        labels = {'tc': 'T.C. *', 'profileImage': 'Profil Resmi'}

        widgets = {


            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'maxlength': '11', 'minlength': '11',
                       'onkeypress': 'validate(event)', 'name': 'tc', 'id': 'tc'}),



        }
