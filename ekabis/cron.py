from datetime import datetime

from django.contrib.auth.models import User

from ekabis.Views.EskalasyonViews import EskalasyonCalculation
from ekabis.models import Menu, YekaCompetition


def my_scheduled_job(request):
    competitions = YekaCompetition.objects.filter(isDeleted=False).filter(eskalasyon_first_date__isnull=False).filter(
        is_calculation=True)
    date = datetime.now().date()
    for competition in competitions:
        compDate = competition.eskalasyon_first_date.split('-')
        if compDate[0] == str(date.month) and compDate[1] == str(date.year):
            result = EskalasyonCalculation(request, competition.uuid)
            print(result)

    print('cron is working')
    pass
