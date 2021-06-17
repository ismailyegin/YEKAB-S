from django import forms
from django.forms import ModelForm

from sbs.models.Products import Products


class ProductSearchForm(ModelForm):
    class Meta:
        model = Products

        fields = (
            'name', 'category', 'suppeliers', 'description')

        labels = {'name': 'Ürün İsmi ', 'category': 'Kategori Seçiniz', 'suppeliers': 'Tedarikçi',
                  'description': 'Açıklama '}

        widgets = {

            'suppeliers': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'name': forms.TextInput(
                attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'category': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),
            'description': forms.TextInput(
                attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

        }

    def __init__(self, *args, **kwargs):
        super(ProductSearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['suppeliers'].required = False
        self.fields['category'].required = False
        self.fields['description'].required = False
