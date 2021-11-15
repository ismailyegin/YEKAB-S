from django.db import models

from ekabis.models import YekaBusiness
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Proposal import Proposal
from ekabis.models.Institution import Institution

class ProposalActive(BaseModel):
    business=models.ForeignKey(YekaBusiness,on_delete=models.CASCADE)
    institution=models.ForeignKey(Institution,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
