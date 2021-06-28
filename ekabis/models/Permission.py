
from django.db import models
from ekabis.models.BaseModel import BaseModel


class Permission(BaseModel):
    name = models.CharField( max_length=255,blank=True,null=True)
    model = models.CharField( max_length=100,blank=True,null=True)
    codename = models.CharField( max_length=100,blank=False,null=False)
    codeurl = models.CharField( max_length=100,blank=False,null=False)
