from django.db import models
from ekabis.models.BaseModel import BaseModel


class FactoryFileName(BaseModel):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return '%s ' % self.name
