class FiltradoPorUsuarioInteligenteMixin:
    """
    Filtra automáticamente el queryset según el lugar de trabajo del usuario:
    - Superusuario ve todo.
    - Usuario autenticado con lugar_de_trabajo ve solo objetos relacionados.
    - Usuario sin lugar_de_trabajo no ve nada.
    
    Detecta automáticamente si el modelo tiene campo 'almacen' o 'lugar_de_trabajo'.
    """
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset.order_by('id')

        lugar = getattr(user, 'lugar_de_trabajo', None)
        if not lugar:
            return queryset.none()

        # Detecta automáticamente el campo a filtrar
        modelo = queryset.model
        campos_modelo = [f.name for f in modelo._meta.fields]
        if 'almacen' in campos_modelo:
            filtro = {'almacen': lugar}
        elif 'lugar_de_trabajo' in campos_modelo:
            filtro = {'lugar_de_trabajo': lugar}
        else:
            # Si el modelo no tiene ningún campo de relación con lugar de trabajo, devuelve todo
            return queryset.order_by('id')

        return queryset.filter(**filtro).order_by('id')
