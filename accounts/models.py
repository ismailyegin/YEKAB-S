import uuid
from django.db import models
from django.contrib.auth.models import User


class Forgot(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
