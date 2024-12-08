from django.apps import AppConfig


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
    # connect signals for automatically creating profile
    def ready(self):
        from . import signals