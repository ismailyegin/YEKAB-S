from django.db import models
from ekabis.models.BaseModel import BaseModel
class CompanyFileNames(BaseModel):
    IsFormal = (
        (True, 'Zorunlu Alan'),
        (False, 'Zorunlu Degil'),
    )
    name = models.CharField(max_length=120, null=True, blank=True)
    is_active=models.BooleanField(default=False,choices=IsFormal)

    def __str__(self):
        return '%s' % self.name


