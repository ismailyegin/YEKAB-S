from django.db import models
from ekabis.models.BaseModel import BaseModel


class City(BaseModel):
    name = models.CharField(max_length=255,blank=True, null=True, verbose_name='Şehir')
    plateNo = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return '%s' % self.name

    def save(self, force_insert=False, force_update=False):
        self.name = self.name.upper()
        super(City, self).save(force_insert, force_update)

    class Meta:
        default_permissions = ()
        # db_table = 'city'
        # managed = False
