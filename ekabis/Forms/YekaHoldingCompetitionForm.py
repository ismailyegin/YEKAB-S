from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import YekaHoldingCompetition


class YekaHoldingCompetitionForm(BaseForm):
    class Meta:
        model = YekaHoldingCompetition

        fields = ('unit',)
        labels = {
            'unit': 'Birimi', }
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),

        }
