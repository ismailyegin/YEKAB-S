from django.db import models


class Country(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Ülke')

    def __str__(self):
        return '%s ' % self.name


    class Meta:
        default_permissions = ()

