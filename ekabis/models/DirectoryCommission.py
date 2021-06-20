from django.db import models


class DirectoryCommission(models.Model):
    name = models.TextField(blank=False, null=False, verbose_name='Kurul Adı')

    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
