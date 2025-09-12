from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, F

from inventarios.models import Inventario
from ventas.models import Venta
from compras.models import Compra


class DashboardView(APIView):
    """
    Muestra métricas globales o filtradas por lugar_de_trabajo:
    - Admin → ve todo
    - Encargado → solo su tienda/almacén
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Filtrado según rol
        if user.is_superuser:
            inventarios = Inventario.objects.all()
            ventas = Venta.objects.all()
            compras = Compra.objects.all()
        elif user.lugar_de_trabajo:
            inventarios = Inventario.objects.filter(almacen=user.lugar_de_trabajo)
            ventas = Venta.objects.filter(tienda=user.lugar_de_trabajo)
            compras = Compra.objects.filter(almacen=user.lugar_de_trabajo)
        else:
            return Response({
                "error": "El usuario no tiene un lugar de trabajo asignado"
            }, status=403)

        data = {
            # 📦 Total stock actual
            "total_stock": inventarios.aggregate(total=Sum("cantidad"))["total"] or 0,

            # 💰 Total de ventas acumuladas
            "total_ventas": ventas.aggregate(total=Sum("total_venta"))["total"] or 0,

            # 🛒 Total de compras acumuladas
            "total_compras": compras.aggregate(total=Sum("total_compra"))["total"] or 0,

            # ⏳ Últimas 5 ventas
            "ventas_recientes": list(
                ventas.order_by("-fecha_creacion")[:5]
                .values("id", "fecha_creacion", "total_venta", "tienda__nombre")
            ),

            # ⏳ Últimas 5 compras
            "compras_recientes": list(
                compras.order_by("-fecha_creacion")[:5]
                .values("id", "fecha_creacion", "total_compra", "almacen__nombre")
            ),

            # ⚠️ Productos con stock bajo
            "alertas_stock": list(
                inventarios.filter(cantidad__lte=F("stock_minimo"))
                .values("producto__nombre", "cantidad", "stock_minimo", "almacen__nombre")
            ),
        }

        return Response(data)
