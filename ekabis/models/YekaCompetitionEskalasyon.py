from django.db import models

from ekabis.models.YekaCompetition import YekaCompetition
from ekabis.models.BaseModel import BaseModel


class YekaCompetitionEskalasyon(BaseModel):
    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, verbose_name='Yeka Yarışması')
    result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Güncel sonuç
    pre_result = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                     blank=True)  # Bir önceki dönem için hesaplanan sonuç
