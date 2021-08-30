from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Newspaper import Newspaper


# BaseForm Hatasına Bakılacak

class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ('listingDate', 'newspaperCount','newspapwerText','file')
        labels = {
            'listingDate': 'İlan Tarihi*',
            'newspaperCount': 'Sayısı*',
            'newspapwerText': 'Açıklama',
            'file':'İlan Metni Dosyası*'
        }
        widgets = {
            'newspaperCount': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)','required': 'required'}),
            'listingDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'newspapwerText': forms.TextInput(attrs={'class': 'form-control '}),



        }
