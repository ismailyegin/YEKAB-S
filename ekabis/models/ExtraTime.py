from django.contrib.auth.models import User, Group
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog

class ExtraTime(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField()
    yeka =models.ForeignKey(Yeka,on_delete=models.CASCADE)
    yekabusinessblog=models.ForeignKey(YekaBusinessBlog,on_delete=models.CASCADE)
