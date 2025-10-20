from django.apps import AppConfig


class InventariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventarios'

class NotificacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notificaciones'

    def ready(self):
        import inventarios.signals  # importa tus señales para stock bajo