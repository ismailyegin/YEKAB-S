from django import forms

from ekabis.models import Company, Person, Employee
from ekabis.models.Yeka import Yeka


class YekaForm(forms.ModelForm):
    class Meta:
        model = Yeka
        fields = ('date', 'definition', 'capacity', 'unit', 'company', 'employee')

        labels = {'definition': 'Tanım ', 'capacity': 'Kapasite', 'company': 'Firma'}
        widgets = {
            'definition': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control '}),

            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),

        }

    company = forms.ModelMultipleChoiceField(queryset=Company.objects.filter(isDeleted=False))
    employee = forms.ModelMultipleChoiceField(queryset=Employee.objects.filter(isDeleted=False))

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)

        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['company'] = [t.pk for t in kwargs['instance'].company.all()]
            self.fields['company'].initial = initial['company']
            initial['employee'] = [t.pk for t in kwargs['instance'].employee.all()]
            self.fields['employee'].initial = initial['employee']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['company'].widget.attrs = {'class': 'select2 select2-hidden-accessible',
                                               'style': 'width: 100%;', 'data-select2-id': '7',
                                               'data-placeholder': 'Firma Seçiniz',}
        self.fields['employee'].widget.attrs = {'class': 'select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'data-select2-id': '8',
                                                'data-placeholder': 'Personel Seçiniz', }
