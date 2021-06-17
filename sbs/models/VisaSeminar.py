import enum

from django.db import models

from sbs.models.Coach import Coach
from sbs.models.Judge import Judge
from sbs.models.EnumFields import EnumFields

from sbs.models.CoachApplication import CoachApplication
from sbs.models.JudgeApplication import JudgeApplication


class VisaSeminar(models.Model):

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

    IsFormal = (
        (True, 'Açık'),
        (False, 'Kapalı'),
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(blank=False, null=False, max_length=1000)
    startDate = models.DateTimeField()
    finishDate = models.DateTimeField()
    location = models.CharField(blank=False, null=False, max_length=1000)
    branch = models.CharField(max_length=128, verbose_name='Branş', choices=EnumFields.BRANCH.value)
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)

    coachApplication = models.ManyToManyField(CoachApplication, related_name='coachApplication')
    judgeApplication = models.ManyToManyField(JudgeApplication, related_name='JudgeApplication')

    coach = models.ManyToManyField(Coach)
    referee = models.ManyToManyField(Judge)
    forWhichClazz = models.CharField(blank=False, null=False, max_length=255)

    application = models.BooleanField(default=False, choices=IsFormal, null=True, blank=True)
    appStartDate = models.DateTimeField(null=True, blank=True)
    appFinishDate = models.DateTimeField(null=True, blank=True)
    year=models.CharField(null=True, blank=True,max_length=20)

    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
