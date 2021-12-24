from django.db import models
from ekabis.models.BaseModel import BaseModel


class Accept(BaseModel):
    date = models.DateField(null=True, blank=True,verbose_name='Kabul Tarihi')
    report = models.FileField(upload_to='kabul/', null=True, blank=True, verbose_name='Kabul Tutanagı')
    installedPower = models.CharField(max_length=100, null=True, blank=True, verbose_name='İşletmedeki Mekanik Güç  (MWm)')
    currentPower = models.CharField(max_length=100, null=True, blank=True,
                                    verbose_name='İşletmedeki Elektiriksel Güç  (MWe)')
