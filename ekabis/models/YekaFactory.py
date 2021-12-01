from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.Factory import Factory
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog


class YekaFactory(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    factory = models.ManyToManyField(Factory)
