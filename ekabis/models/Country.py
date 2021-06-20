from django.db import models


class Country(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='Ülke')

    def __str__(self):
        return '%s ' % self.name

    def save(self, force_insert=False, force_update=False):
        self.name = self.name.upper()
        super(Country, self).save(force_insert, force_update)

    class Meta:
        default_permissions = ()
        db_table = 'country'
        managed = False
