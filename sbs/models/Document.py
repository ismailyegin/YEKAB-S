from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to='document/', null=False, blank=False, verbose_name='Document')
    name = models.CharField(blank=False, null=False, max_length=1000)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '%s ' % self.name
