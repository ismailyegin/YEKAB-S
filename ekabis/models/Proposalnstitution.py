from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.File import File
from ekabis.models.Institution import Institution


class ProposalInstitution(BaseModel):
    status = models.CharField(max_length=100, default='Sonuçlanmadı')
    file = models.FileField(upload_to='KurumGorus/', null=True, blank=True, verbose_name='Kurum Görüsleri')
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
    date = models.DateField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True, verbose_name='Kurum Görüşü Öneri Sayısı')

    def __str__(self):
        return '%s' % (self.institution.name)
