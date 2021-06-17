from django import forms
from django.forms import ModelForm
from sbs.models import SportClubUser
from sbs.models.CategoryItem import CategoryItem

from sbs.models.PreRegistration import PreRegistration


class PreRegistrationForm(ModelForm):
    kademe_definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'),
                                               to_field_name='name',
                                               empty_label="Seçiniz",
                                               required=False,
                                               label="Kademe",
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control select2 ',
                                                          'style': 'width: 100%; '}))

    class Meta:
        model = PreRegistration

        fields = (
            'tc', 'profileImage', 'height', 'weight', 'birthDate', 'bloodType', 'gender', 'birthplace', 'motherName',
            'fatherName', 'first_name', 'last_name', 'email', 'is_active', 'phoneNumber', 'address', 'postalCode',
            'phoneNumber2', 'city', 'country', 'name', 'shortName', 'foundingDate', 'logo', 'clubMail', 'isFormal',
            'clubphoneNumber', 'clubaddress', 'clubpostalCode', 'clubphoneNumber2', 'clubcity', 'clubcountry',
            'petition', 'role', 'isCoach', 'kademe_belge', 'kademe_startDate', 'iban', 'kademe_definition')
        labels = {'tc': 'T.C.', 'gender': 'Cinsiyet', 'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email',
                  'phoneNumber': 'Cep Telefonu',
                  'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu', 'city': 'İl', 'country': 'Ülke',
                  'name': 'Adı', 'shortName': 'Kısa Adı',
                  'foundingDate': 'Kuruluş Tarihi', 'clubMail': 'Email', 'isFormal': 'Kulüp Türü', 'role': 'Kulüp Rolü',
                  'clubphoneNumber': 'Cep Telefonu', 'clubphoneNumber2': 'Sabit Telefon',
                  'isCoach': 'Aynı zaman da kulup Antrenörü müsünüz?',
                  'kademe_belge': 'Antrenörlük Belgesi Yükleyiniz: ', 'kademe_startDate': 'Kademe Başlangıç Zamanı ',
                  'iban': 'iban adresini giriniz'}

        widgets = {

            'iban': forms.TextInput(
                attrs={'id': 'iban', 'class': 'form-control  iban',
                       'onkeyup': 'if(this.value.length > 34){this.value=this.value.substr(0, 34);}', 'value': ''}),

            'kademe_startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'off',
                        }),

            'isCoach': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; ', 'required': 'required'}),
            'isFormal': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'required': 'required'}),
            'role': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),

            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"}),

            'shortName': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control'}),

            'foundingDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'off',
                       'required': 'required'}),

            'clubaddress': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', "style": "text-transform:uppercase"}),

            'clubphoneNumber': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'clubphoneNumber2': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'clubpostalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'clubcity': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;',
                       'required': 'required'}),

            'clubcountry': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;',
                       'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control '}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),

            'tc': forms.TextInput(attrs={'class': 'form-control ',
                                         'onkeyup': 'if(this.value.length >11){this.value=this.value.substr(0, 11);}',
                                         'id': 'tc',
                                         'onkeypress': 'return isNumberKey(event)',
                                         'value': '',
                                         'required': 'required'}),

            'height': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'weight': forms.TextInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required',
                       "style": "text-transform:uppercase"}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker', 'autocomplete': 'off',
                        'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),


        }
