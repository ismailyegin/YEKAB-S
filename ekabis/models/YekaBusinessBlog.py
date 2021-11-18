from django.db import models

from ekabis.models.Company import Company
from ekabis.models.BaseModel import BaseModel
from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre


class YekaBusinessBlog(BaseModel):
    INDEFINETE_CHOICES = (
        (True, 'Süresiz '),
        (False, 'Süreli')
    )
    businessblog = models.ForeignKey(BusinessBlog, on_delete=models.CASCADE, null=True, blank=True) #iş planında bulunan bir bloğun sabit bilgileri
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='business_parent', null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    finisDate = models.DateTimeField(null=True, blank=True)
    businessTime = models.IntegerField(null=True, blank=True)
    time_type = models.CharField(null=True, blank=True, max_length=100)
    status = models.CharField(max_length=100, null=True, blank=True, default='Başlanmadı')
    sorting = models.IntegerField(default=0)
    companies = models.ManyToManyField(Company)
    parameter = models.ManyToManyField(YekaBusinessBlogParemetre, null=True, blank=True) #dinamik parametre bilgileri
    indefinite = models.BooleanField(default=False, choices=INDEFINETE_CHOICES)
    explanation = models.CharField(max_length=250,null=True, blank=True)
    dependence_parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='depence_parent', null=True,
                                          blank=True)
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name='Tamamlanma Tarihi')

    def __str__(self):
        return '%s' % (self.businessblog.name)
