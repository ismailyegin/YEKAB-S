from django.db import models

from sbs.models.Abirim import Abirim
from unicode_tr import unicode_tr
class AbirimParametre(models.Model):
    aDate = 'date'
    aString = 'string'
    aNumber = 'number'
    aYear='year'

    Type = (
        (aDate, 'Tarih'),
        (aString, 'Metin'),
        (aNumber, 'Sayi'),
        ( aYear,'Yil')

    )

    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=120,  null=True, blank=True, verbose_name='Başlık')
    type = models.CharField(max_length=128, verbose_name='Türü ', choices=Type,default=aString)
    birim = models.ForeignKey(Abirim, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Birim')
    kobilid=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return '%s' % (self.title)


    def save(self, force_insert=False, force_update=False):
        if self.title:
            self.title = unicode_tr(self.title)
            self.title = self.title.upper()

        super(AbirimParametre, self).save(force_insert, force_update)