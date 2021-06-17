from django.db import models


class Branch(models.Model):
    name = models.CharField(blank=True, null=True, max_length=120, verbose_name='Branş Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
