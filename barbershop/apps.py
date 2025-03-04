from django.apps import AppConfig


class BarbershopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'barbershop'
    verbose_name = 'Салон красоты'

    def ready(self):
        import barbershop.signals  # Импортируем сигналы
