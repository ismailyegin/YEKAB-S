from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler

from ekabis.cron import my_scheduled_job


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_scheduled_job, 'interval', minutes=1)
    scheduler.start()