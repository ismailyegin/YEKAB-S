import uuid
from django.db import models
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    isDeleted = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Set this model as Abstract