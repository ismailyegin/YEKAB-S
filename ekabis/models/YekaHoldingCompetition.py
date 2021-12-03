from django.db import models

from ekabis.models import ConnectionUnit
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Factory import Factory
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog

#Yarışmanın yapılması iş bloğunda Yarışma Tavan fiyatı için birim kayıt edilmekte
class YekaHoldingCompetition(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    unit=models.ForeignKey(ConnectionUnit,on_delete=models.DO_NOTHING,null=True,blank=True)
    max_price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)

