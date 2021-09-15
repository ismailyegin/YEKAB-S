from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.CompetitionCompany import CompetitionCompany

class Competition(BaseModel):#Yarışmaların yapılması iş bloğu

    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE)

    company=models.ManyToManyField(CompetitionCompany)

    report=models.FileField(upload_to='yarisma/', null=True, blank=True)

    date = models.DateField(null=True, blank=True,verbose_name='Yarisma Tarihi')



