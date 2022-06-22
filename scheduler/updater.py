
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from ekabis.cron import my_scheduled_job


def start():
    scheduler = BackgroundScheduler(timezone='Europe/Istanbul')
    # cron1 = CronTrigger(day_of_week='mon-fri', hour='10', minute='34,35,36', timezone='Europe/Istanbul')
    cron2 = CronTrigger(day_of_week='mon-fri', hour='00', minute='00', timezone='Europe/Istanbul')

    trigger = OrTrigger([cron2])
    scheduler.add_job(my_scheduled_job, trigger)
    scheduler.start()
