from django.db import models

from ekabis.models.BaseModel import BaseModel


class   BusinessBlogParametreType(BaseModel):
    aDate = 'date'
    aString = 'string'
    aNumber = 'number'
    aYear = 'year'
    afile = 'file'
    Type = (
        (aDate, 'Tarih'),
        (aString, 'Metin'),
        (aNumber, 'Sayi'),
        (aYear, 'Yil'),
        (afile, 'Dosya'),

    )
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name='Başlık')
    type = models.CharField(max_length=128, verbose_name='Türü ', choices=Type, default=aString)
