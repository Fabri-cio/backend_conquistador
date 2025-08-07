from django.utils import timezone
from rest_framework import viewsets

class AuditableModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base que gestiona automáticamente los campos
    usuario_creacion, usuario_modificacion y fecha_modificacion.
    """
    def perform_create(self, serializer):
        serializer.save(usuario_creacion=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            usuario_modificacion=self.request.user,
            fecha_modificacion=timezone.now()
        )
