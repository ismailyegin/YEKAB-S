import enum

from django.db import models

from sbs.models.Coach import Coach
from sbs.models.Judge import Judge
from sbs.models.EnumFields import EnumFields


class CoachApplication(models.Model):
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
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    coach = models.ForeignKey(Coach, on_delete=models.DO_NOTHING, null=False, blank=False)
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='coachApplication ')

    def __str__(self):
        return '%s ' % self.coach

    class Meta:
        default_permissions = ()
