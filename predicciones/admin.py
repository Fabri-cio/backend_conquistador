from django.contrib import admin
from .models import Prediccion, DetallePrediccion, ConfiguracionModelo

# Register your models here.
admin.site.register(Prediccion)
admin.site.register(DetallePrediccion)
admin.site.register(ConfiguracionModelo)

