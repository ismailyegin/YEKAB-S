from django.db import models


class Penal(models.Model):
    file = models.FileField(upload_to='Penal/', null=True, blank=True, verbose_name='Penal')
    penal = models.CharField(blank=False, null=False, max_length=1000)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '%s ' % self.penal
