
from django.db import models
from ekabis.models.BaseModel import BaseModel

class YekaApplicationFileName(BaseModel):
    filename = models.CharField(blank=True, null=True, max_length=250)



