from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetallePrediccion
from .services import PrediccionService

@receiver(post_save, sender=DetallePrediccion)
@receiver(post_delete, sender=DetallePrediccion)
def actualizar_resultado_signal(sender, instance, **kwargs):
    PrediccionService.actualizar_resultado(instance.prediccion)
