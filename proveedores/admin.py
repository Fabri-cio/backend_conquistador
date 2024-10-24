from django.contrib import admin
from .models import DetalleOrden, OrdenCompra, Proveedor

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOrden)