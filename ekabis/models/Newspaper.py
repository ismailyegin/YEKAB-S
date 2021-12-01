from django.contrib.auth.models import User, Group
from django.db import models
from unicode_tr import unicode_tr

from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog



class Newspaper(BaseModel):
    business = models.ForeignKey(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    listingDate=models.DateField(null=True, blank=True)
    newspaperCount=models.CharField(max_length=120,blank=True, null=True)
    newspapwerText=models.TextField(blank=True, null=True)
    file=models.FileField()
