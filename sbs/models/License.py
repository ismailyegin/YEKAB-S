import enum

from django.db import models

from sbs.models.Coach import Coach
from sbs.models.City import City
from sbs.models.EnumFields import EnumFields
from sbs.models.SportsClub import SportsClub


class License(models.Model):
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
    operationDate = models.DateTimeField(auto_now=True)

    branch = models.CharField(max_length=128, verbose_name='Branş', choices=EnumFields.BRANCH.value, null=True,
                              blank=True)
    sportsClub = models.ForeignKey(SportsClub, on_delete=models.CASCADE, db_column='sportsClub')
    isActive = models.BooleanField(default=False)
    licenseNo = models.CharField(blank=True, null=True, max_length=255)
    expireDate = models.DateField(blank=True, null=True)
    cityHeadShip = models.ForeignKey(City, on_delete=models.CASCADE, db_column='cityHeadShip', null=True, blank=True)
    startDate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    lisansPhoto = models.FileField(upload_to='lisans/', null=True, blank=True, verbose_name='Lisans')
    reddetwhy = models.CharField(blank=True, null=True, max_length=255)
    isFerdi = models.BooleanField(default=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, blank=True, null=True, related_name="antrenor1")
    coach2 = models.ForeignKey(Coach, on_delete=models.SET_NULL, blank=True, null=True, related_name="antrenor2")

    def __str__(self):
        return '%s ' % self.sportsClub.name

    def save(self, force_insert=False, force_update=False):
        if self.branch:
            self.branch = EnumFields.BADMİNTON.value
        super(License, self).save(force_insert, force_update)

    # class Meta:
    #     default_permissions = ()
    #     db_table = 'license'
