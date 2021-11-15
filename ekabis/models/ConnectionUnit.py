import uuid
from django.db import models

from ekabis.models.BaseModel import BaseModel


class ConnectionUnit(BaseModel):
    name = models.TextField(blank=False, null=False, verbose_name='Birim')

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
