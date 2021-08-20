from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import FactoryFile
from ekabis.models.FactoryFileName import FactoryFileName

file_names = FactoryFileName.objects.filter(isDeleted=False)


class FactoryFileForm(BaseForm):
    class Meta:
        model = FactoryFile
        fields = ('name', 'file',)
        labels = {'file': 'Doküman', 'name': 'Doküman Kategori', }
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'name': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

        }

    def __init__(self, *args, **kwargs):
        super(FactoryFileForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['name'].queryset = FactoryFileName.objects.filter(isDeleted=False)
