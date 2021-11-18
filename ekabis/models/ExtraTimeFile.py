from django.contrib.auth.models import User, Group
from django.db import models
from ekabis.models.BaseModel import BaseModel


class ExtraTimeFile(BaseModel):
    definition = models.CharField(blank=True, null=True, max_length=250)
    file=models.FileField(null=False,blank=False)

    def __str__(self):
        return '%s' % self.definition