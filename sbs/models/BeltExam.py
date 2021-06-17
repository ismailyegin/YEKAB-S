from django.db import models

from sbs.models import Coach, Athlete, CategoryItem, SportsClub, Level, License
from sbs.models.EnumFields import EnumFields


class BeltExam(models.Model):
    BANK = 'Banka'
    POSTA = 'Posta'
    PAYMENT_CHOICES = (
        (BANK, 'Banka'),
        (POSTA, 'Posta'),
    )
    WAITED = 'Beklemede'
    APPROVED = 'Onaylandı'
    PROPOUND = 'Onaya Gönderildi'
    DENIED = 'Reddedildi'

    STATUS_CHOICES = (
        (APPROVED, 'Onaylandı'),
        (PROPOUND, 'Onaya Gönderildi'),
        (DENIED, 'Reddedildi'),
        (WAITED, 'Beklemede'),
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    examDate = models.DateField(null=False, blank=False)

    coachs = models.ManyToManyField(Coach)


    paymentType = models.CharField(max_length=128, verbose_name='Ödeme Şekli', choices=PAYMENT_CHOICES, default=BANK)
    dekont = models.FileField(upload_to='dekont/', null=False, blank=False, verbose_name='Dekont ')
    dekontDate = models.DateField(null=True, blank=True)
    dekontDescription = models.CharField(max_length=255, null=True, blank=True)
    athletes = models.ManyToManyField(Athlete)
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    sportClub = models.ForeignKey(SportsClub, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    branch = models.CharField(max_length=128, choices=EnumFields.BRANCH.value, null=False, blank=False)

    class Meta:
        default_permissions = ()
