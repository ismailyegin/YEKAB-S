from django.db import models

from ekabis.models.BaseModel import BaseModel


class Eskalasyon(BaseModel):
    series = models.CharField(null=False, blank=False, verbose_name='Seri Kodu',max_length=100) #örn: TP.DK.USD.A
    startDate = models.CharField(null=False, blank=False, max_length=100)
    endDate = models.CharField(null=False, blank=False, max_length=100)
    key = models.CharField(null=False, blank=False, max_length=100,verbose_name='Merkez Bankası API Key')
    aggregationTypes=models.CharField(null=False, blank=False, max_length=100,verbose_name='Matematiksel Fonsiyon İşlemi') #örn: avg
    formulas=models.CharField(null=False, blank=False, max_length=100,verbose_name='Formül Parametresi') #örn Düzey için: 0
    frequency=models.CharField(null=False, blank=False, max_length=100,verbose_name='Frekans Parametresi') #örn Günlük için : 1
    result=models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    result_description=models.CharField(max_length=250,null=True,blank=True,verbose_name='Sonuç Açıklaması')





