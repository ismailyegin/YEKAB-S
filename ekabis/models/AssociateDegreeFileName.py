
from django.db import models
from ekabis.models.BaseModel import BaseModel

class AssociateDegreeFileName(BaseModel):
    name = models.CharField(blank=True, null=True, max_length=250)

    def __str__(self):
        return '%s ' % self.name



