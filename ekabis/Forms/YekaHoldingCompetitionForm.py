from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import YekaHoldingCompetition


class YekaHoldingCompetitionForm(BaseForm):
    class Meta:
        model = YekaHoldingCompetition

        fields = ('unit', 'max_price',)
        labels = {
            'unit': 'Para Birimi',
            'max_price': 'Yarışma Tavan Fiyatı', }
        widgets = {
            'unit': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;'}),
            'max_price': forms.NumberInput(
                attrs={'class': 'form-control'}),

        }
