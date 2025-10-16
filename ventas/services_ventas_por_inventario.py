from ventas.models import DetalleVenta
from django.db.models import Sum

def obtener_ventas_por_inventario(inventario_id, fecha_inicio=None, fecha_fin=None):
    """
    Retorna la cantidad vendida por día para un inventario específico,
    usando la fecha completa (datetime) tal como está en la base de datos.
    """
    ventas_qs = DetalleVenta.objects.filter(inventario_id=inventario_id)

    if fecha_inicio:
        ventas_qs = ventas_qs.filter(venta__fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        ventas_qs = ventas_qs.filter(venta__fecha_creacion__lte=fecha_fin)

    # Agrupamos por venta__fecha_creacion sin truncar
    ventas = (
        ventas_qs
        .values('venta__fecha_creacion')
        .annotate(cantidad_total=Sum('cantidad'))
        .order_by('venta__fecha_creacion')
    )

    # Solo devolvemos el valor original
    return [{"fecha": v["venta__fecha_creacion"], "cantidad": float(v["cantidad_total"])} for v in ventas]
