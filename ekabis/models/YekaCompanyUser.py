
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaUser import YekaUser

class YekaCompanyUser(BaseModel):

    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE)
    companyuser=models.ManyToManyField(YekaUser)