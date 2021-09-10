from ekabis.models.BaseModel import BaseModel
from django.db import models
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType


class BusinessBlog(BaseModel): #Sabit tanımlanan iş bloğu isim ve parametreler
    name = models.CharField(max_length=255, null=False, blank=False,unique=True)
    parametre=models.ManyToManyField(BusinessBlogParametreType,null=True,blank=True)
    start_notification=models.IntegerField(null=True,blank=True)
    finish_notification=models.IntegerField(null=True,blank=True)

