from django.db import models
from unicode_tr import unicode_tr

class Abirim(models.Model):

    name = models.CharField(max_length=120, null=True, blank=True, verbose_name='İsim')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    kobilid=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return '%s' % (self.name)

    def save(self, force_insert=False, force_update=False):
        if self.name:
            self.name = unicode_tr(self.name)
            self.name = self.name.upper()

        super(Abirim, self).save(force_insert, force_update)
