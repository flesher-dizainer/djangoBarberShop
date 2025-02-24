from django.apps import AppConfig


class BarbershopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'barbershop'

    def ready(self):
        import barbershop.signals  # Импортируем сигналы