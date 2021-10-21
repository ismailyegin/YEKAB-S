from django.db import models

from ekabis.models.BaseModel import BaseModel

class Coordinate(BaseModel):
    y = models.DecimalField(blank=False, null=False, max_digits=9, decimal_places=6)
    x = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=6)
