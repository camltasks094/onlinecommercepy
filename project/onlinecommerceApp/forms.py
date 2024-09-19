from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Tienda, Inventario, Carrito, Reseña
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import Producto, Solicitud

class CrearUsuarioForm(UserCreationForm):
    ROLE_CHOICES = (
        ('comprador', 'Comprador'),
        ('tendero', 'Tendero'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol')

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'role', 'telefono', 'fecha_nacimiento', 'first_name',
                  'last_name']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )



class ProductForm(forms.ModelForm):
    # Agregar un campo para la cantidad del inventario
    cantidad_inventario = forms.IntegerField(min_value=0, label='Cantidad en Inventario', required=True)

    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion', 'precio', 'fecha_vencimiento', 'id_categoria_producto', 'imagen', 'cantidad_inventario']

    def save(self, commit=True):
        # Sobrescribir el método save para manejar la cantidad de inventario
        producto = super().save(commit=False)
        if commit:
            producto.save()
        return producto




class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tienda
        fields = ['nombre', 'telefono', 'descripcion', 'correo', 'instagram', 'id_categoria', 'id_direccion', 'imagen']




class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_producto', 'cantidad']




class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['nombre','correo', 'telefono', 'asunto','descripcion', 'id_tipo_solicitud']




class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }
