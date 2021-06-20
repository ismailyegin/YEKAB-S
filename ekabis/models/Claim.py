import enum

from django.db import models

from sbs.models.Coach import Coach
from sbs.models.Judge import Judge
from sbs.models.EnumFields import EnumFields


class Claim(models.Model):
    WAITED = 'Beklemede'
    APPROVED = 'Onaylandı'
    PROPOUND = 'İşlem Devam Ediliyor'
    DENIED = 'Reddedildi'

    STATUS_CHOICES = (
        (APPROVED, 'Onaylandı'),
        (PROPOUND, 'İşlem Devam Ediliyor'),
        (DENIED, 'Reddedildi'),
        (WAITED, 'Beklemede'),
    )

    SBS = 'BİLGİ SİSTEMİ'
    MOBİL = 'MOBİL UYGULAMA'
    WEBSİTE = 'WEB SİTE'



    ACİL = 'ACİL'
    ONEMLİ = 'ÖNEMLİ'
    AZONEMLİ = 'AZ ÖNEMLİ'

    STATUS_PROJECT = (
        (SBS, 'BİLGİ SİSTEMİ'),
        (MOBİL, 'MOBİL UYGULAMA'),
        (WEBSİTE, 'WEB SİTE'),
    )

    İMPORTANCE = (
        (ACİL, 'ACİL'),
        (ONEMLİ, 'ÖNEMLİ'),
        (AZONEMLİ, 'AZ ÖNEMLİ'),
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    # baslık
    title = models.CharField(blank=False, null=False, max_length=1000)
    # proje durumu
    project = models.CharField(max_length=128, verbose_name='Proje Seçiniz', choices=STATUS_PROJECT, default=SBS)
    # proje durumu
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    # proje açıklama
    definition = models.CharField(blank=False, null=False, max_length=1000)
    # önem durumu
    importanceSort = models.CharField(max_length=128, verbose_name='Önem Durumu', choices=İMPORTANCE, default=ACİL)
    # ücret
    pay = models.IntegerField(blank=True, null=True)
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return '%s ' % self.title

    # class Meta:
    #     default_permissions=()
