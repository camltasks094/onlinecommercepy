from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Producto, CategoriaProducto

User = get_user_model()


class ProductoModelTest(TestCase):

    def setUp(self):
        # Crear un usuario para los campos relacionados
        self.usuario_creacion = User.objects.create_user(
            username='creador',
            password='password123',
            email='creador@example.com'
        )
        self.usuario_modificacion = User.objects.create_user(
            username='modificador',
            password='password456',
            email='modificador@example.com'
        )

        # Crear una categoría de producto
        self.categoria = CategoriaProducto.objects.create(
            nombre='Electrónica'
        )

        # Crear un producto
        self.producto = Producto.objects.create(
            nombre_producto='Smartphone',
            descripcion='Un smartphone de última generación.',
            precio=699.99,
            fecha_vencimiento=timezone.now().date(),
            id_categoria_producto=self.categoria,
            id_usuario_creacion=self.usuario_creacion,
            id_usuario_modificacion=self.usuario_modificacion
        )

    def test_producto_creation(self):
        """Verificar que el producto se creó correctamente"""
        self.assertEqual(self.producto.nombre_producto, 'Smartphone')
        self.assertEqual(self.producto.descripcion, 'Un smartphone de última generación.')
        self.assertEqual(self.producto.precio, 699.99)
        self.assertEqual(self.producto.id_categoria_producto.nombre, 'Electrónica')
        self.assertEqual(self.producto.id_usuario_creacion.username, 'creador')
        self.assertEqual(self.producto.id_usuario_modificacion.username, 'modificador')

    def test_producto_str_method(self):
        """Verificar el método __str__ del producto"""
        self.assertEqual(str(self.producto), 'Smartphone')

    def test_producto_related_category(self):
        """Verificar la relación con la categoría"""
        self.assertEqual(self.producto.id_categoria_producto, self.categoria)

    def test_producto_fecha_modificado_default(self):
        """Verificar que la fecha modificado es igual a la fecha de creación por defecto"""
        self.assertEqual(self.producto.fecha_modificado, self.producto.fecha_creacion)

    def test_producto_image_field(self):
        """Verificar el campo de imagen del producto"""
        self.assertIsNone(self.producto.imagen)

