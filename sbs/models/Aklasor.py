
from django.db import models

from sbs.models.CategoryItem import CategoryItem
from sbs.models.Abirim import Abirim
from unicode_tr import unicode_tr

class Aklasor(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Tanımı')
    sirano = models.IntegerField(null=False, blank=False,verbose_name='Sıra Numarası')
    location = models.ForeignKey(CategoryItem, on_delete=models.SET_NULL,null=True, blank=True,verbose_name='Konumu')
    birim = models.ForeignKey(Abirim, on_delete=models.CASCADE,null=True, blank=True,verbose_name='Birim')
    startyear = models.IntegerField(null=True, blank=True, verbose_name=' Başlangıç Yılı')
    finishyear=models.IntegerField(null=True, blank=True, verbose_name='Bitiş Yılı')
    kobilid=models.IntegerField(null=True,blank=True)



    def __str__(self):
        return '%s ' % self.name


    def save(self, force_insert=False, force_update=False):
        if self.name:
            self.name = unicode_tr(self.name)
            self.name = self.name.upper()

        super(Aklasor, self).save(force_insert, force_update)








