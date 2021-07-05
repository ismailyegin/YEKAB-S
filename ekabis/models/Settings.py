from django.db import models
from ekabis.models.BaseModel import BaseModel


class Settings(models.Model):
    key = models.CharField(blank=True, null=True,max_length=120)
    value = models.CharField(blank=True, null=True, max_length=120)
    is_active = models.BooleanField(default=False)
    label = models.CharField(blank=True, null=True, max_length=250)
