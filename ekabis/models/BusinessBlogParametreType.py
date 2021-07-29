from django.db import models
from ekabis.models.BaseModel import BaseModel
class  BusinessBlogParametreType(BaseModel):
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
    necesssary_choices = (
        (True, 'Zorunlu '),
        (False, 'Zorunlu Degil')
    )
    COMPANY_CHOICES = (
        (True, 'Evet '),
        (False, 'Hayır')
    )
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name='Başlık')
    type = models.CharField(max_length=128, verbose_name='Türü ', choices=Type, default=aString)
    necessary=models.BooleanField(default=False,choices=necesssary_choices)
    companynecessary = models.BooleanField(default=False,choices=COMPANY_CHOICES)
