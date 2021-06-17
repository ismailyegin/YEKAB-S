from urllib import request

from random import choices
from django.db import models
from sbs.models.EnumFields import EnumFields


class CategoryItem(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)
    forWhichClazz = models.CharField(blank=False, null=False, max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.CharField(max_length=128, choices=EnumFields.BRANCH.value, null=True, blank=True,
                              verbose_name='Seçiniz')
    isFirst = models.BooleanField(null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    kobilid=models.IntegerField(null=True,blank=True)

    def locationSet(self, location, deger):
        deger =  str(location.name)+"/"+deger
        if not (location.parent):
            return '%s' % (str(deger))
        else:
            location = CategoryItem.objects.get(pk=location.parent_id)
            return self.locationSet(location, deger)

    def __str__(self):
        if self.parent == None:
            return '%s' % (self.name)
        else:
            location = CategoryItem.objects.get(pk=self.parent_id)
            return '%s' % ( self.locationSet( location, '')+self.name )

    # class Meta:
    #     default_permissions = ()
    #     db_table = 'categoryitem'
    #     managed = False
