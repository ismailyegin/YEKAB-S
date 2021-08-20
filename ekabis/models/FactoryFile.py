from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.FactoryFileName import FactoryFileName


class FactoryFile(BaseModel):
    file = models.FileField(upload_to='fabrika-dokumani/', null=False, blank=False, verbose_name='Fabrika Dokümanı')
    name = models.ForeignKey(FactoryFileName, null=False, blank=False, on_delete=models.DO_NOTHING)
