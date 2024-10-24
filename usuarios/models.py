from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Campo opcional para el teléfono
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Campo opcional para la dirección
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación, se establece automáticamente

    def __str__(self):
        return self.username  # Retorna el nombre de usuario al convertir a string
