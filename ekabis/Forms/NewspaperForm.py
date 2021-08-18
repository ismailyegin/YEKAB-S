from django import forms
from ekabis.models.Newspaper import Newspaper


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ('listingDate', 'newspaperCount','newspapwerText','file')
        labels = {
            'listingDate': 'İlan Tarihi',
            'newspaperCount': 'Sayısı',
            'newspapwerText': 'İlan Metni',
            'file':'Dosyası'
        }
        widgets = {
            'newspaperCount': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'listingDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'newspapwerText': forms.TextInput(attrs={'class': 'form-control '}),



        }
