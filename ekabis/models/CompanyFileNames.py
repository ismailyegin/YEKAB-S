from django.db import models
from ekabis.models.BaseModel import BaseModel
class CompanyFileNames(BaseModel):
    name = models.CharField(max_length=120, null=True, blank=True)
    is_active=models.BooleanField(default=False)



