
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from ekabis.cron import my_scheduled_job, eskalasyon_date_job


def start():
    scheduler = BackgroundScheduler(timezone='Europe/Istanbul')
    # cron1 = CronTrigger(day_of_week='mon-fri', hour='10', minute='34,35,36', timezone='Europe/Istanbul')
    cron2 = CronTrigger(day_of_week='mon-fri', hour='00', minute='00',month='7' ,timezone='Europe/Istanbul') #ESKALASYON HESAPLANMASI
    cron3 = CronTrigger(hour='16', minute='50,55',month='7' ,timezone='Europe/Istanbul') #ÖNCEKİ YARIŞMALARA AİT ESKALASYON TARİHLERİNİN GÜNCELLENMESİ

    trigger = OrTrigger([cron2])
    trigger3 = OrTrigger([cron3])

    scheduler.add_job(my_scheduled_job, trigger)
    scheduler.add_job(eskalasyon_date_job, trigger3)

    scheduler.start()
