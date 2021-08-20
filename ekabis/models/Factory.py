from django.db import models

from ekabis.models import FactoryFile
from ekabis.models.BaseModel import BaseModel


class Factory(BaseModel):
    date = models.DateField()
    name = models.CharField(max_length=120, null=False, blank=False)
    file = models.ManyToManyField(FactoryFile)
