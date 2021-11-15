from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.File import File
from ekabis.models.Institution import Institution


class ProposalInstitution(BaseModel):
    Choices = (
        (True, 'Onaylandı '),
        (False, 'Beklemede'),

    )
    status=models.BooleanField(choices=Choices,default=False)
    file=models.FileField(upload_to='KurumGorus/', null=True, blank=True, verbose_name='Kurum Görüsleri')
    institution=models.ForeignKey(Institution,on_delete=models.CASCADE)
    date=models.DateField(null=True,blank=True)
