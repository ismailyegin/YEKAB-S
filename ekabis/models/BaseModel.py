import uuid
from django.db import models
from django.http import request



class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    isDeleted = models.BooleanField(default=False, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modificationDate = models.DateTimeField(auto_now=True, null=True, blank=True)
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        abstract = True  # Set this model as Abstract

    # def save(self, *args, **kwargs):
    #     request = kwargs.get('request', None)
    #     model = self._meta.object_name
    #     model_log(request,self)
