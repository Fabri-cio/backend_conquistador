from imagekit.processors import ResizeToFill
from PIL import Image

class SkipIfWebP(ResizeToFill):
    """
    Procesador que omite el procesamiento si la imagen ya es WebP.
    """
    def process(self, image):
        # Si la imagen ya está en formato WebP, la dejamos igual
        if image.format and image.format.lower() == "webp":
            return image
        # Caso contrario, hacemos el ResizeToFill normal
        return super().process(image)
