from django import forms
from django.forms import ModelForm

from sbs.models import BeltExam, SportsClub


class BeltExamForm(ModelForm):
    sportClub = forms.ModelChoiceField(queryset=SportsClub.objects.all(),
                                       to_field_name='name',
                                       empty_label="Seçiniz",
                                       label="Kulüp",
                                       required=True,
                                       widget=forms.Select(
                                           attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%; '}))



    class Meta:
        model = BeltExam

        fields = (
            'examDate', 'paymentType', 'dekont', 'sportClub', 'branch')

        labels = {'examDate': 'Sınav Tarihi', 'paymentType': 'Ücret Gönderim Şekli',
                  'dekont': 'Dekont', 'sportClub': 'Kulüp', 'branch': 'Branch'}

        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'examDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'off',
                        'required': 'required'}),

            'paymentType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%; ', 'required': 'required'}),

            'dekont': forms.FileInput()

        }
