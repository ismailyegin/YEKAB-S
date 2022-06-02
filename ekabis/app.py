from django.apps import AppConfig


class EkabisConfig(AppConfig):
    name = 'ekabis'

    def ready(self):
        from scheduler import updater
        updater.start()