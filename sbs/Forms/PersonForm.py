from django import forms
from django.forms import ModelForm
from sbs.models.Nationnality import Nationnality

from sbs.models import Person


class PersonForm(ModelForm):

    class Meta:
        model = Person

        fields = (
            'tc', 'profileImage',
            'height', 'weight',
            'birthDate', 'bloodType',
            'gender', 'birthplace',
            'motherName',
            'uyrukid',
            'profileImage', 'fatherName',
            'meslek', 'kurum', 'is_unvani',
            'education', 'mezunokul',
            'nufus_ailesirano',
            'nufus_sirano',
            'nufus_ciltno',
            'uyrukid')

        labels = {'tc': 'T.C*.',
                  'gender': 'Cinsiyet*',
                  'profileImage': 'Profil Resmi',


                  'nufus_ailesirano': 'Nufus Aile Sıra No',
                  'nufus_sirano': 'Nufus Sıra No',
                  'nufus_ciltno': 'Nufus Cilt No',
                  'kurum': 'kurum',
                  'is_unvani': 'İs Unvanı ',
                  'education': 'Eğitim',
                  'mezunokul': 'Mezun Okul ',
                  'meslek': 'Meslek',
                  'height': 'Boy',
                  'weight': 'Kilo',
                  'uyrukid':'Uyruk',

                  }

        widgets = {

            'profileImage': forms.FileInput(),

            'is_unvani': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

            'nufus_ailesirano': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'nufus_sirano': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'nufus_ciltno': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'kurum': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'meslek': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'tc': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', 'onkeypress': 'validate(event)',
                       'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                       'placeholder': ""}),

            'height': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'weight': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                        'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
            'education': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;'}),
            'mezunokul': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),
            'uyrukid': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;','required': 'required'}),

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
