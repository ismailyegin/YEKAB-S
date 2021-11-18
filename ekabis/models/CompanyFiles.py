from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.CompanyFileNames import CompanyFileNames
class CompanyFiles(BaseModel):

    filename=models.ForeignKey(CompanyFileNames,on_delete=models.CASCADE)
    file = models.FileField(upload_to='company/', null=True, blank=True,verbose_name='company_files')

    def __str__(self):
        return '%s' % self.filename