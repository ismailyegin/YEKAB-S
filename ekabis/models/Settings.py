from django.db import models
from ekabis.models.BaseModel import BaseModel


class Settings(models.Model):
    Active = (
        (True, 'True '),
        (False, 'False')
    )
    key = models.CharField(blank=True, null=True,max_length=120)
    value = models.CharField(blank=True, null=True, max_length=120)
    label = models.CharField(blank=True, null=True, max_length=250)
    explanation=models.CharField(blank=True, null=True, max_length=500)

