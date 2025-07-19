from django.contrib import admin
from .models import Pedido, DetallePedido, RecepcionPedido, DetalleRecepcion, Compra

# Register your models here.
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(RecepcionPedido)
admin.site.register(DetalleRecepcion)
admin.site.register(Compra)

