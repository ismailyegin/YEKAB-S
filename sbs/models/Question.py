from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=400, null=True, blank=True)
    isActiv = models.BooleanField(null=True, blank=True, default=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    reaply = models.CharField(max_length=400, null=True, blank=True)
    count = models.IntegerField()
