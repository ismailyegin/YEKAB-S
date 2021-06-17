from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from sbs.models.CategoryItem import CategoryItem
from sbs.models.EnumFields import EnumFields


class CoachSearchForm(ModelForm):
    # kademe
    definition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kademe",
                                        required=False,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))
    branch = forms.ChoiceField(choices=EnumFields.BRANCH.value,
                               label="Kademe", widget=forms.Select(
            attrs={'class': 'form-control select2 select2-hidden-accessible',
                   'style': 'width: 100%; ',
                   }))

    #  'onchange': 'this.form.submit()' ile ajax yazilabilir not
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active',)
        labels = {'first_name': 'Ad', 'last_name': 'Soyad'}
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Ad', 'value': '',
                       }),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyad', }),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),

        }
