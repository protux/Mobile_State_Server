from django.apps import AppConfig


class PhoneConfig(AppConfig):
    name = 'mosta.phone'

    def ready(self):
        from . import signals
