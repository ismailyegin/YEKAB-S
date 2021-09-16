from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import YekaPurchaseGuarantee

choices = (
    ('---','---'),
    ('Süre', 'Süre'),
    ('Miktar', 'Miktar')
)


class PurchaseGuaranteeForm(BaseForm):
    class Meta:
        model = YekaPurchaseGuarantee
        fields = ('type', 'time', 'total_quantity',)
        labels = {
            'type': 'Alım Garantisi Türü',
            'time': 'Alım Garanti Süresi (Süreyi Ay Olarak Giriniz)',
            'total_quantity': 'Toplam Üretim Miktarı (GWh)'}
        widgets = {
            'type': forms.Select(choices=choices, attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                           'style': 'width: 100%;'}),
            'time': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'total_quantity': forms.NumberInput(
                attrs={'class': 'form-control'}),

        }

