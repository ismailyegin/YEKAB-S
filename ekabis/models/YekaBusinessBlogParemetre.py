from django.db import models

from ekabis.models import Company
from ekabis.models.BaseModel import BaseModel
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType


class YekaBusinessBlogParemetre(
    BaseModel):  # dinamik oluşturulan parametre için tutulan değerler örn(parametre = resmi gazete ilan tarihi ,value:01/01/2021)
    value = models.CharField(max_length=120, null=True, blank=True, verbose_name='value')
    parametre = models.ForeignKey(BusinessBlogParametreType, on_delete=models.SET_NULL, null=True,
                                  blank=True)  # text,date,number seçimleri
    file = models.FileField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True,
                                blank=True)  # secilen parametre hangi şirkete ait (suan kullanılmıyor)
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name='parametre adı')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.parametre:
            self.title = self.parametre.title
            super(YekaBusinessBlogParemetre, self).save(force_insert, force_update)
