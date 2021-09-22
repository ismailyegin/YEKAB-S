from django.db import models


class FileExtension(models.Model):
    extension = models.CharField(max_length=100, null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
