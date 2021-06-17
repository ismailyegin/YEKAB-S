from django import forms
from django.forms import ModelForm

from sbs.models import Communication
from sbs.models.Country import Country


class CommunicationForm(ModelForm):
    # country = forms.ModelChoiceField(queryset=Country.objects.all(),
    #                                  to_field_name='name',
    #                                  empty_label="Seçiniz",
    #                                  label="Ülke",
    #                                  initial=Country.objects.filter(name="TÜRKİYE")[0],
    #                                  # required=True,
    #                                  widget=forms.Select(
    #                                      attrs={'class': 'form-control select2 select2-hidden-accessible',
    #                                             'style': 'width: 100%; '}))
    class Meta:

        model = Communication

        fields = (
            'phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'country', 'city', 'phoneHome', 'phoneJop',
            'addressHome', 'addressJop')
        labels = {'phoneNumber': 'Cep Telefonu',
                  'phoneNumber2': 'Sabit Telefon',
                  'phoneHome': 'Ev Telefonu',
                  'phoneJop': 'İş Telefonu',
                  'addressHome': 'Ev Adresi',
                  'addressJop': 'İş Adresi',
                  'postalCode': 'Posta Kodu',
                  'city': 'İl', }
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', "style": "text-transform:uppercase"}),
            'addressHome': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', "style": "text-transform:uppercase"}),
            'addressJop': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', "style": "text-transform:uppercase"}),

            'phoneNumber': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;'}),

            'phoneHome': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'phoneJop': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

        }
