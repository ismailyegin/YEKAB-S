from django.db import models
from ekabis.models.BaseModel import BaseModel


class Budget(BaseModel):
    budgetDate = models.DateField(null=True, blank=True, verbose_name='Tarih')
    budgetFile = models.FileField(upload_to='butce/', null=True, blank=True, verbose_name='Bütçe Dokümanı')
    annualSpendAmount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,
                                            verbose_name='Yıılık Harcanan Miktar')
