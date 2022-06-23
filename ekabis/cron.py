import trace
import traceback
from datetime import datetime

from django.contrib.auth.models import User
from django.http import request

from ekabis.Views.EskalasyonViews import EskalasyonCalculation
from ekabis.Views.YekaCompetitionViews import competitionEskalasyonDate
from ekabis.models import YekaCompetition, Notification, NotificationUser


def my_scheduled_job():
    try:
        print(datetime.now())
        competitions = YekaCompetition.objects.filter(isDeleted=False).filter(
            eskalasyon_first_date__isnull=False).filter(is_calculation=True)
        date = datetime.now().date()
        for competition in competitions:
            compDate = competition.eskalasyon_first_date.split('-')
            if str(date.month) and compDate[1] == str(date.year) :
                EskalasyonCalculation(competition.uuid)
    except:
        traceback.print_exc()


def eskalasyon_date_job():
    try:
        print('eskalasyon date ')
        notification=Notification(not_description='TEST CRON NOTIFICATION',title=str(datetime.today())+'--CRONJOB')
        notification.save()
        NotificationUser(user=User.objects.filter(is_superuser=True).last(),notification=notification).save()
        # yekas = YekaCompetition.objects.filter(isDeleted=False).order_by('-date')
        # competitionEskalasyonDate(yekas)
    except:
        traceback.print_exc()