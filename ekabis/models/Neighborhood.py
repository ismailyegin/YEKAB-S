from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.District import District


class Neighborhood(BaseModel):
    name = models.TextField(blank=True, null=True, verbose_name='Mahalle Adı')
    district = models.ForeignKey(District, blank=True, null=True, verbose_name='İlçe', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.name
