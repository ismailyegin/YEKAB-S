from django.db import models
from unicode_tr import unicode_tr

from ekabis.models import ConnectionRegion
from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness

class Yeka(BaseModel):
    definition = models.CharField(blank=True, null=True, max_length=250)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    capacity = models.IntegerField(blank=True, null=True)
    yekaParent = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)
    unit = models.ForeignKey(ConnectionUnit, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_parent = models.BooleanField(default=False, null=True, blank=True)
    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE,null=True,blank=True)
    connection_region=models.ManyToManyField(ConnectionRegion)

    def __str__(self):
        return '%s ' % self.definition

    def save(self, force_insert=False, force_update=False):
        if self.definition:
            self.definition = unicode_tr(self.definition).upper()

        super(Yeka, self).save(force_insert, force_update)