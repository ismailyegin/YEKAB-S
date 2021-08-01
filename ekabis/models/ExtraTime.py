from django.contrib.auth.models import User, Group
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.ExtraTimeFile import ExtraTimeFile

class ExtraTime(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField()
    business =models.ForeignKey(YekaBusiness,on_delete=models.CASCADE)
    yekabusinessblog=models.ForeignKey(YekaBusinessBlog,on_delete=models.CASCADE)
    files=models.ManyToManyField(ExtraTimeFile)
