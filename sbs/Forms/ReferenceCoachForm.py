from django import forms
from sbs.models.ReferenceCoach import ReferenceCoach
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from sbs.models.CategoryItem import CategoryItem


class RefereeCoachForm(ModelForm):
    kademe_definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'),
                                               to_field_name='name',
                                               empty_label="Seçiniz",
                                               label="Kademe",
                                               required='required',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                          'style': 'width: 100%; '}))

    class Meta:
        model = ReferenceCoach
        fields = (
            'first_name', 'last_name', 'email', 'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city',
            'country', 'iban', 'tc', 'profileImage', 'birthDate', 'bloodType', 'gender', 'birthplace', 'motherName',
            'fatherName', 'kademe_belge', 'kademe_startDate')



        labels = {'iban': 'İban Adresi', 'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email',
                  'phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke', 'tc': 'T.C.', 'gender': 'Cinsiyet',
                  'kademe_belge': 'Antrenörlük Belgesi Yükleyiniz:',
                  'kademe_startDate': 'Kademe Başlangıç Zamanı ', }
        widgets = {

            'tc': forms.TextInput(attrs={'class': 'form-control ',
                                         'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                                         'id': 'tc',
                                         'onkeypress': 'return isNumberKey(event)',
                                         'value': '',
                                         'required': 'required'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),
            'iban': forms.TextInput(
                attrs={'id': 'iban', 'class': 'form-control  iban',
                       'onkeyup': 'if(this.value.length > 34){this.value=this.value.substr(0, 34);}', 'value': '',
                       'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                       'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', "style": "text-transform:uppercase"}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),
            'kademe_startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'off',
                        'required': 'required'}),

        }

    def clean_email(self):

        data = self.cleaned_data['email']
        print(self.instance)
        if self.instance.id is None:
            if User.objects.filter(email=data).exists():
                raise forms.ValidationError("Bu email başka bir kullanıcı tarafından kullanılmaktadır.")
            return data
        else:
            return data

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
