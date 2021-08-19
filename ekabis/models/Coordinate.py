from django.db import models

from ekabis.models.BaseModel import BaseModel

class Coordinate(BaseModel):
    y = models.CharField(blank=True, null=True,max_length=120)
    x = models.CharField(null=True,blank=True,max_length=120)