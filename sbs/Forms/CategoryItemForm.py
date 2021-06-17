from django import forms
from django.forms import ModelForm

from sbs.models import CategoryItem


class CategoryItemForm(ModelForm):
    class Meta:
        model = CategoryItem
        fields = ('name', 'parent', 'branch', 'isFirst')
        labels = {'name': 'Tanımı', 'branch': 'Branş', 'isFirst': 'İlk Kuşak mı ?', 'parent': 'Üst Kuşak'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
            'isFirst': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),
            'parent': forms.Select(choices=[], attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                      'style': 'width: 100%;', })
        }

        def __init__(self, *args, **kwargs):
            super(CategoryItemForm, self).__init__(*args, **kwargs)
            self.fields['parent'].empty_label = 'Seçiniz'
            self.fields['parent'].choices = CategoryItem.objects.filter(forWhichClazz='BELT').values_list("name",
                                                                                                          "name").distinct()
        def branch(self):
            return self.branch()
