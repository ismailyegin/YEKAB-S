
from django.db import models
from ekabis.models.BaseModel import BaseModel

class Settings(BaseModel):
    logincount = models.IntegerField(blank=False, null=False)
    capchakey= models.CharField(blank=True, null=True, max_length=120)
    is_active=models.BooleanField(default=False)


