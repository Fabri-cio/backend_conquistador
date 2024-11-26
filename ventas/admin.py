from django.contrib import admin
from .models import Venta, DetalleVenta  # Elimina Cliente de aquí

# Registra los modelos en el admin
admin.site.register(Venta)
admin.site.register(DetalleVenta)
