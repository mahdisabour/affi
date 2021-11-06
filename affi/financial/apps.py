from django.apps import AppConfig


class FinancialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'affi.financial'

    def ready(self) -> None:
        from . import signals
        return super().ready()
