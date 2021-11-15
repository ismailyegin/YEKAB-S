from django.db import models
from unicode_tr import unicode_tr

from ekabis.models import YekaCompetition
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.CompetitionCompany import CompetitionCompany

class Competition(BaseModel):#Yarışmaların yapılması iş bloğu

    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE)

    company=models.ManyToManyField(CompetitionCompany)

    report=models.FileField(upload_to='yarisma/', null=True, blank=True)

    date = models.DateField(null=True, blank=True,verbose_name='Yarisma Tarihi')


    def save(self, force_insert=False, force_update=False):
        super(Competition, self).save(force_insert, force_update)
        if YekaCompetition.objects.filter(business=self.business):
            competition=YekaCompetition.objects.get(business=self.business)
            if not competition.eskalasyon_first_date:
                date = self.date
                if date.month == 1 or date.month == 2 or date.month == 3:
                    competition.eskalasyon_first_date = '07-' + str(date.year)
                elif date.month == 4 or date.month == 5 or date.month == 6:
                    competition.eskalasyon_first_date = '10-' + str(date.year)
                elif date.month == 7 or date.month == 8 or date.month == 9:
                    competition.eskalasyon_first_date = '01-' + str(date.year)
                elif date.month == 10 or date.month == 11 or date.month == 12:
                    competition.eskalasyon_first_date = '04-' + str(date.year)
                competition.save()

        super(Competition, self).save(force_insert, force_update)

