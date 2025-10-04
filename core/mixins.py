class FiltradoPorUsuarioInteligenteMixin:
    """
    Filtra automáticamente el queryset según el lugar de trabajo del usuario:
    - Superusuario ve todo.
    - Usuario autenticado con lugar_de_trabajo ve solo objetos relacionados.
    - Usuario sin lugar_de_trabajo no ve nada.

    Funciona para:
    - Campos directos: 'almacen', 'lugar_de_trabajo'
    - Relaciones FK: por ejemplo 'inventario__almacen'
    """
    # Lista de campos a buscar en el modelo o en relaciones FK
    FILTROS_POR_DEFECTO = ['almacen', 'lugar_de_trabajo']

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

        modelo = queryset.model
        campos_modelo = [f.name for f in modelo._meta.fields]

        filtro_aplicado = None

        # 1️⃣ Revisar campos directos
        for campo in self.FILTROS_POR_DEFECTO:
            if campo in campos_modelo:
                filtro_aplicado = {campo: lugar}
                break

        # 2️⃣ Revisar relaciones FK si no encontró campo directo
        if not filtro_aplicado:
            for campo in self.FILTROS_POR_DEFECTO:
                for f in modelo._meta.fields:
                    if f.is_relation and f.many_to_one:
                        # Construir filtro tipo 'fk__almacen'
                        if hasattr(f.related_model, campo):
                            filtro_aplicado = {f"{f.name}__{campo}": lugar}
                            break
                if filtro_aplicado:
                    break

        # 3️⃣ Si no encontró ningún campo ni relación, devuelve todo
        if not filtro_aplicado:
            return queryset.order_by('id')

        return queryset.filter(**filtro_aplicado).order_by('id')
