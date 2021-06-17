import enum

from django.db import models

from sbs.models.City import City
from sbs.models.EnumFields import EnumFields
from sbs.models.CategoryItem import CategoryItem


class Level(models.Model):
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

    levelType = models.CharField(max_length=128, verbose_name='Leveller', choices=EnumFields.LEVELTYPE.value)
    branch = models.CharField(max_length=128, verbose_name='Branş', choices=EnumFields.BRANCH.value, null=True,
                              blank=True)
    isActive = models.BooleanField(default=False)
    startDate = models.DateField(null=True, blank=True)
    expireDate = models.DateField(null=True, blank=True, )
    durationDay = models.IntegerField(null=True, blank=True, )
    definition = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)

    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='Belge ')
    # son eklemeler
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', null=True, blank=True)
    form = models.FileField(upload_to='form/', null=True, blank=True, verbose_name='Form ')

    def __str__(self):
        return '%s ' % self.levelType

    def save(self, force_insert=False, force_update=False):
        if self.branch:
            self.branch = EnumFields.BADMİNTON.value
        super(Level, self).save(force_insert, force_update)

    # class Meta:
    #     default_permissions = ()
