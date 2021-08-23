
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.CompanyUser import CompanyUser
class YekaUser(BaseModel):

    user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    startDate=models.DateField(null=True, blank=True,verbose_name='Başlama Tarihi')
    finisDate=models.DateField(null=True, blank=True,verbose_name='Bitiş  Tarihi')
    file=models.FileField(upload_to='CompanyUser/', null=True, blank=True, verbose_name='Atama Yazısı')