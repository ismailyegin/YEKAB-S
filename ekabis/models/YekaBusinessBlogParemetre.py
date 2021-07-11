from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType

class YekaBusinessBlogParemetre(BaseModel):
    value = models.CharField(max_length=120, null=True, blank=True, verbose_name='value')
    parametre = models.ForeignKey(BusinessBlogParametreType, on_delete=models.SET_NULL, null=True, blank=True)
    file =models.FileField(null=True,blank=True)
