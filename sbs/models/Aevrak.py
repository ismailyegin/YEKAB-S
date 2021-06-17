from django.db import models
class Aevrak(models.Model):
    file = models.FileField(null=False, blank=False, max_length=1000)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    kobilid=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return '%s ' % self.file