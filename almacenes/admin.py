from django.contrib import admin
from .models import Almacen, Inventario, Movimiento, TipoMovimiento

# Register your models here.
admin.site.register(Almacen)
admin.site.register(TipoMovimiento)
admin.site.register(Inventario)
admin.site.register(Movimiento)