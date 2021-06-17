from django import forms
from django.forms import ModelForm

from sbs.models import Level, CategoryItem
from sbs.models.EnumFields import EnumFields


class BeltForm(ModelForm):
    definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='BELT'),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Tanımı",
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))

    class Meta:
        model = Level

        fields = (
            'startDate', 'definition', 'city', 'form', 'dekont',)

        labels = {'startDate': 'Hak Kazanma Tarihi'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'off',
                       }),
            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

        }
