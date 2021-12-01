from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.ProduceAmount import ProduceAmount
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog


class YekaProduceAmount(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING) #iş planı
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING) #iş planına ait iş bloğu
    amount = models.ManyToManyField(ProduceAmount, null=True, blank=True, verbose_name='Üretim Miktarı')
