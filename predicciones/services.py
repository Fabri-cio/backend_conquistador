from django.db.models import Sum
from .models import Prediccion

class PrediccionService:
    @staticmethod
    def actualizar_resultado(prediccion: Prediccion):
        total = prediccion.detalles.aggregate(total=Sum("cantidad"))["total"] or 0
        prediccion.resultado = total
        prediccion.save(update_fields=["resultado"])
