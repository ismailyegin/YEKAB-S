from ekabis.models.BaseModel import BaseModel
from django.db import models
from ekabis.models.BusinessBlog import BusinessBlog


class YekaBusinessBlog(BaseModel):
    businessblog=models.ForeignKey(BusinessBlog,on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    startDate=models.DateTimeField(null=True, blank=True)
    finisDate=models.DateTimeField(null=True, blank=True)
    businessTime=models.IntegerField(null=True, blank=True)
    status=models.BooleanField(default=False)