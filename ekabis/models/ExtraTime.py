from django.contrib.auth.models import User, Group
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.ExtraTimeFile import ExtraTimeFile


class ExtraTime(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.IntegerField()
    business = models.ForeignKey(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    files = models.ManyToManyField(ExtraTimeFile)
    time_type = models.CharField(null=True, blank=True, max_length=100)
    definition=models.CharField(null=True,blank=True,max_length=250)
    new_date=models.DateField(null=True,blank=True)
