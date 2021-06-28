from django.contrib.auth.models import User
from django.db import models
from ekabis.models.BaseModel import BaseModel
class Notification(BaseModel):
    notification = models.CharField(blank=True, null=True, max_length=200, verbose_name='Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    users = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)
    is_show = models.BooleanField(default=False)
    entityId = models.IntegerField()
    tableName = models.CharField(blank=True, null=True, max_length=120)
    kobilid = models.IntegerField(null=True, blank=True, default=1)
    def __str__(self):
        return '%s ' % self.notification

