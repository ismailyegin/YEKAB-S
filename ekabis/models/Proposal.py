from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.Coordinate import Coordinate
from ekabis.models.Location import Location
from ekabis.models.Proposalnstitution import ProposalInstitution

# Aday Yeka yekanın lokasyonun da öneri
from ekabis.services.services import validate_file_extension, validate_file_size


class Proposal(BaseModel):
    capacity = models.IntegerField(blank=True, null=True)
    information_form = models.FileField(upload_to='information/', null=True, blank=True,validators=[validate_file_size])
    date = models.DateField(null=True, blank=True)
    coordinate = models.ManyToManyField(Coordinate)
    location = models.ManyToManyField(Location)
    farm_form = models.FileField(null=True, blank=True,validators=[validate_file_size])
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=250, blank=False, null=False, verbose_name='Aday Yeka')
    # Kurum önerileri
    institution = models.ManyToManyField(ProposalInstitution)
    kml_file = models.FileField(null=True, blank=True, verbose_name='KML Dosyası', upload_to="aday_yeka/",
                                validators=[validate_file_extension])

    def __str__(self):
        return '%s' % self.name

