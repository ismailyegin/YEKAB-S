from django.db import models

from sbs.models.AbirimParametre import AbirimParametre
from sbs.models.Adosya import Adosya
from unicode_tr import unicode_tr

class AdosyaParametre(models.Model):

    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=120, null=True, blank=True, verbose_name='value')
    dosya = models.ForeignKey(Adosya, on_delete=models.CASCADE,null=False, blank=False)
    parametre=models.ForeignKey(AbirimParametre,on_delete=models.CASCADE,null=True, blank=True)
    kobilid=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return '%s' % (self.value)


    def save(self, force_insert=False, force_update=False):
        if self.value:
            self.value = unicode_tr(self.value)
            self.value = self.value.upper()

        super(AdosyaParametre, self).save(force_insert, force_update)