from django import forms
from django.forms import ModelForm

from sbs.models.Products import Products


class ProductForm(ModelForm):
    class Meta:
        model = Products

        fields = (
            'name', 'category', 'stock', 'suppeliers', 'description')

        labels = {'name': 'Ürün İsmi ', 'category': 'Kategori Seçiniz', 'suppeliers': 'Tedarikçi',
                  'stock': 'Stok Adeti', 'description': 'Açıklama '}

        widgets = {

            'suppeliers': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}),

            'stock': forms.TextInput(attrs={'class': 'form-control', "onkeypress": "return isNumberKey(event)"}),
            'category': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),
            'description': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2', "style": "text-transform:uppercase"}),

        }
