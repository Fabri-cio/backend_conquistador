from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from rest_framework import serializers

class ImagenThumbMixin(models.Model):
    imagen_thumb = ImageSpecField(
        source='imagen',
        processors=[ResizeToFill(200, 200)],
        format='WEBP',
        options={'quality': 80}
    )

    class Meta:
        abstract = True

class ImageThumbMixinSerializer:

    def get_image_url(self, obj, field='imagen_thumb', related_obj=None):
        """
        Devuelve la URL de la miniatura cacheada de la imagen.
        - obj: objeto actual (Inventario, Producto, etc.)
        - field: nombre del atributo ImageSpecField (por defecto 'imagen_thumb')
        - related_obj: si la imagen está en un objeto relacionado (por ejemplo producto)
        """
        target = related_obj if related_obj else obj
        if hasattr(target, field) and getattr(target, field):
            url = getattr(target, field).url
            ts = int(getattr(target, "fecha_modificacion", 0).timestamp()) if hasattr(target, "fecha_modificacion") else 0
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(f"{url}?v={ts}")
            return f"{url}?v={ts}"
        return None
