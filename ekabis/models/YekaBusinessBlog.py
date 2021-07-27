from django.db import models

from ekabis.models.Company import Company
from ekabis.models.BaseModel import BaseModel
from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre


class YekaBusinessBlog(BaseModel):
    TRUE_FALSE_CHOICES = (
        (True, 'Aktif'),
        (False, 'Pasif')
    )
    INDEFINETE_CHOICES = (
        (True, 'SÜRESİZ '),
        (False, 'SÜRELİ')
    )
    businessblog = models.ForeignKey(BusinessBlog, on_delete=models.CASCADE,null=True,blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    finisDate = models.DateTimeField(null=True, blank=True)
    businessTime = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False ,choices=TRUE_FALSE_CHOICES)
    sorting = models.IntegerField(default=0)
    companys=models.ManyToManyField(Company)
    paremetre=models.ManyToManyField(YekaBusinessBlogParemetre,null=True,blank=True)
    indefinite=models.BooleanField(default=False,choices=INDEFINETE_CHOICES)
