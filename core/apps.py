from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        print("Importing Signals from Core APP")
        import core.signals

