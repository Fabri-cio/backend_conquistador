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

    def get_image_url(self, obj):
        request = self.context.get("request")
        if hasattr(obj, "imagen_thumb") and obj.imagen_thumb:
            url = obj.imagen_thumb.url
            ts = int(getattr(obj, "fecha_modificacion", 0).timestamp()) if hasattr(obj, "fecha_modificacion") else 0
            return request.build_absolute_uri(f"{url}?v={ts}")
        return None
