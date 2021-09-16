from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaPerson import YekaPerson
from ekabis.models.Employee import Employee


class YekaPersonForm(BaseForm):
    class Meta:
        model = YekaPerson
        fields = ('employee','yeka')

    employee = forms.ModelMultipleChoiceField(queryset=Employee.objects.filter(isDeleted=False))

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            forms.ModelForm.__init__(self, *args, **kwargs)
            initial['employee'] = [t.pk for t in kwargs['instance'].employee.all()]
            self.fields['employee'].initial = initial['employee']

        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['employee'].widget.attrs = {'class': 'select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'data-select2-id': '8',
                                                'data-placeholder': 'Personel Seçiniz', }
