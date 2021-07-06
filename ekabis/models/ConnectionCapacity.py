from django.db import models

from ekabis.models.ConnectionRegion import ConnectionRegion
from ekabis.models.BaseModel import BaseModel
from ekabis.models.ConnectionUnit import ConnectionUnit


class ConnectionCapacity(BaseModel):
    name = models.TextField(blank=False, null=False, verbose_name='Bağlantı Kapasitesi')
    value = models.IntegerField(null=False, blank=False, verbose_name='Miktar')
    unit = models.ForeignKey(ConnectionUnit, on_delete=models.DO_NOTHING, verbose_name='Birim', null=False, blank=False)
    connection_region = models.ForeignKey(ConnectionRegion, on_delete=models.DO_NOTHING,
                                            verbose_name='Bağlantı Bölgesi', null=True, blank=True)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
