from django.db import models
from ekabis.models.BaseModel import BaseModel
class File(BaseModel):
    file = models.FileField()