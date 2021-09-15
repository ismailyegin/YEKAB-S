from django.db import models

from ekabis.models.BaseModel import BaseModel


class ProduceAmount(BaseModel):
    date = models.DateField(null=True, blank=True, verbose_name='Tarih')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Miktar(GWh)')

