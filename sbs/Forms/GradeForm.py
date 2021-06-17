from django import forms
from django.forms import ModelForm

from sbs.models.CategoryItem import CategoryItem
from sbs.models.Level import Level
from sbs.models.EnumFields import EnumFields


class GradeForm(ModelForm):
    definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kademe",
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))

    class Meta:
        model = Level

        fields = (
            'startDate', 'definition', 'dekont', 'branch')

        labels = {'startDate': 'Hak Kazanma Tarihi', 'branch': 'Branş'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'off',
                       }),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
