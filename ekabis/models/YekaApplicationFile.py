from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaApplicationFileName import YekaApplicationFileName

class YekaApplicationFile(BaseModel):
    filename = models.ForeignKey(YekaApplicationFileName,on_delete=models.CASCADE)
    file=models.FileField(null=True,blank=True)
