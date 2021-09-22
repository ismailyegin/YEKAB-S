from django.contrib.auth.models import User
from django.db import models

from ekabis.models.YekaCompetition import YekaCompetition
from ekabis.models.Eskalasyon import Eskalasyon
from ekabis.models.BaseModel import BaseModel


class YekaCompetitionEskalasyon(BaseModel):
    eskalasyon_info = models.ManyToManyField(Eskalasyon,verbose_name='Eskalasyon Formül Bilgileri ',null=True,blank=True) # Formuldeki her bir alt formüllerin sonuç ve bilgileri
    competition = models.ForeignKey(YekaCompetition, on_delete=models.CASCADE, verbose_name='Yeka Yarışması')
    result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # Güncel sonuç
    pre_result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) #Bir önceki dönem için hesaplanan sonuç

