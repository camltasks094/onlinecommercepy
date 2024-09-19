from django.urls import path
from .views import register, login_view, DashboardView, ProductCreateView, ProductListView, ProductDetailView, \
    ProductDeleteView, ProductUpdateView, TiendaCreateView, TiendaListView, TiendaDetailView, TiendaUpdateView, \
    TiendaDeleteView, InventarioCreateView, InventarioListView, InventarioDeleteView, \
    InventarioUpdateView, inicioView, CarritoView, agregar_producto, CarritoDeleteView, logout, logoutView, \
    SolicitudCreateView, ListarSolicitudView, ReseñaCreateView, exportar_inventario
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('', inicioView, name="inicio"),
    path('about/', views.AboutView, name="about"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logoutView, name="logout"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('product/create/', ProductCreateView.as_view(), name='crear_producto'),
    path('product/', ProductListView.as_view(), name='listar_producto'),
    path('product/detail/<int:pk>', ProductDetailView.as_view(), name="detalle_producto"),
    path('product/delete<int:pk>', ProductDeleteView.as_view(), name="borrar_producto"),
    path('product/update<int:pk>', ProductUpdateView.as_view(), name="actualizar_producto"),
    path('tienda/create/', TiendaCreateView.as_view(), name='crear_tienda'),
    path('tienda/listar/', TiendaListView.as_view(), name="listar_tienda" ),
    path('tienda/<int:pk>/', TiendaDetailView.as_view(), name='detalle_tienda'),
    path('tienda/editar/<int:pk>/', TiendaUpdateView.as_view(), name='editar_tienda'),
    path('tienda/eliminar/<int:pk>/', TiendaDeleteView.as_view(), name='eliminar_tienda'),
    path('tienda/<int:tienda_id>/inventario/agregar/', InventarioCreateView.as_view(), name='agregar_inventario'),
    path('tienda/<int:tienda_id>/inventario/', InventarioListView.as_view(), name='listar_inventario'),
    path('inventario/<int:pk>/actualizar/', InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario/<int:pk>/eliminar/', InventarioDeleteView.as_view(), name='inventario_delete'),
    path('inventario/exportar/<int:tienda_id>/', exportar_inventario, name='exportar_inventario'),

    path('agregar_producto/<int:producto_id>/', agregar_producto, name='agregar_producto'),
    path('carrito/', CarritoView, name='carrito'),
    path('eliminar-producto/<int:pk>/', CarritoDeleteView.as_view(), name='eliminar_producto'),
    path('solicitud/crear/<int:tienda_id>/', SolicitudCreateView.as_view(), name='solicitud'),
    path('tienda/<int:tienda_id>/solicitudes/', ListarSolicitudView.as_view(), name='listarSolicitudes'),
    path('reseña/crear/<int:tienda_id>/', ReseñaCreateView.as_view(), name='reseña'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

