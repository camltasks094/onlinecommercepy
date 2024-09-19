
# Register your models here.
from django.contrib import admin
from .models import Usuario, CategoriaTienda, Solicitud, TipoSolicitud, ProductoHasVenta, Ventas, ProductoHasPedido, \
    Inventario, InteraccionSolicitud, DetalleFisico, DetalleDomicilio, Pagos, MetodoPago, Pedido, Carrito, Tienda, \
    Producto, Reseña
from .models import CategoriaProducto

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefono', 'fecha_nacimiento', 'cedula', 'tipo_cedula', 'genero', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Tienda)
admin.site.register(Pedido)
admin.site.register(MetodoPago)
admin.site.register(Pagos)
admin.site.register(DetalleDomicilio)
admin.site.register(DetalleFisico)
admin.site.register(InteraccionSolicitud)
admin.site.register(Inventario)
admin.site.register(ProductoHasPedido)
admin.site.register(Ventas)
admin.site.register(ProductoHasVenta)
admin.site.register(Solicitud)
admin.site.register(TipoSolicitud)
admin.site.register(Reseña)



@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre')
    search_fields = ('nombre',)

@admin.register(CategoriaTienda)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre')
    search_fields = ('nombre',)


