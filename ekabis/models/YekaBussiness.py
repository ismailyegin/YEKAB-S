from ekabis.models.BaseModel import BaseModel
from django.db import models
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog

class YekaBusiness(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='YekaBusiness')
    businessblogs=models.ManyToManyField(YekaBusinessBlog)

