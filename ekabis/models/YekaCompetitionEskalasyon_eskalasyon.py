from django.db import models

from ekabis.models.YekaCompetitionEskalasyon import YekaCompetitionEskalasyon
from ekabis.models.Eskalasyon import Eskalasyon
from ekabis.models.BaseModel import BaseModel


class YekaCompetitionEskalasyon_eskalasyon(BaseModel):
    eskalasyon_info = models.ForeignKey(Eskalasyon, null=True, blank=True,
                                        on_delete=models.CASCADE)  # Formuldeki her bir alt formüllerin sonuç ve bilgileri
    yeka_competition_eskalasyon = models.ForeignKey(YekaCompetitionEskalasyon, on_delete=models.CASCADE, null=True,
                                                    blank=True)  # yeka yarışması eskalasyonu
