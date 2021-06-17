from django import forms
from django.forms import ModelForm

from sbs.models import CategoryItem


class AcategoriForm(ModelForm):


    parent = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='location'),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Üst Konumu",
                                        required=False,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))


    class Meta:
        model = CategoryItem
        fields = ('name', 'parent')
        labels = {'name': 'Tanımı',}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),

            # 'isFirst': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),
            'parent': forms.Select(choices=[], attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                      'style': 'width: 100%;', })
        }

