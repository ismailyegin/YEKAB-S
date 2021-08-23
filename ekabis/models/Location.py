from django.db import models

from ekabis.models import Neighborhood
from ekabis.models.BaseModel import BaseModel
from ekabis.models.City import City
from ekabis.models.District import District


class Location(BaseModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, max_length=120, null=True, blank=True, on_delete=models.DO_NOTHING)
