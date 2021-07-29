from ekabis.models.BaseModel import BaseModel
from django.db import models
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType


class BusinessBlog(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    parametre=models.ManyToManyField(BusinessBlogParametreType,null=True,blank=True)
    start_notification=models.IntegerField(null=True,blank=True)
    finish_notification=models.IntegerField(null=True,blank=True)

