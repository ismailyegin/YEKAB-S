from django import forms
from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Budget import Budget



class BudgetForm(BaseForm):
    class Meta:
        model = Budget
        fields = ('budgetFile','budgetDate','annualSpendAmount',)
        labels = {'budgetDate': 'Tarih',
                  'annualSpendAmount': 'Yıllık Harcanan Miktar',
                  }
        widgets = {
            'annualSpendAmount': forms.NumberInput(
                attrs={'class': 'form-control ','required':'required'}),
            'budgetDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ','required':'required', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),

        }