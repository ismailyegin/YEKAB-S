from django import forms
from django.forms import ModelForm

from ekabis.models.Person import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage', 'height', 'weight', 'birthDate', 'bloodType', 'gender', 'birthplace', 'motherName',
            'fatherName')
        labels = {'tc': 'T.C.', 'gender': 'Cinsiyet','profileImage':'Profil Resmi'}

        widgets = {
            'profileImage': forms.FileInput(),

            'tc': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'height': forms.TextInput(attrs={'class': 'form-control'}),

            'weight': forms.TextInput(attrs={'class': 'form-control'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'required': 'required'}),

        }

    def clean_tc(self):

        data = self.cleaned_data['tc']
        print(self.instance)
        if self.instance is None:
            if Person.objects.filter(tc=data).exists():
                raise forms.ValidationError("This tc already used")
            return data
        else:
            return data
