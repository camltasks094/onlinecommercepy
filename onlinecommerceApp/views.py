import random
from datetime import date
import csv  # Añade esta línea para importar el módulo csv
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from .forms import LoginForm, TiendaForm, InventarioForm, SolicitudForm, ReseñaForm
from .forms import CrearUsuarioForm, ProductForm
from .models import Producto, Tienda, Inventario, Carrito, Usuario, Solicitud, Reseña, CategoriaProducto
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin



class TenderoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Tendero').exists()


class DashboardView(TenderoRequiredMixin, TemplateView):

    template_name = 'dashboard.html'


def register(request):

    if request.method == 'POST': # Verifica si la solicitud es de tipo POST
        form = CrearUsuarioForm(request.POST) # Crea una instancia del formulario con los datos del POST
        if form.is_valid():
            user = form.save() # Guarda el usuario en la base de datos
            role = form.cleaned_data.get('role') # Solo asigna el usuario al grupo si se eligió un rol
            if role:
                if role == 'comprador':
                    group = Group.objects.get(name='Comprador')
                elif role == 'tendero':
                    group = Group.objects.get(name='Tendero')
                user.groups.add(group) # Añade el usuario al grupo correspondiente
            login(request, user) # Inicia sesión al usuario recién registrado
            return redirect('inicio')
    else:
        form = CrearUsuarioForm()
    # Renderiza la plantilla 'register.html' pasando el formulario como contexto
    return render(request, 'register.html', {'form': form})




def inicioView(request):

    if request.user.is_authenticated:
        nombre_usuario = request.user.username
    else:
        nombre_usuario = "Invitado"

    productos = list(Producto.objects.all())
    productos_aleatorios = random.sample(productos, min(len(productos), 5))
    context = {
        'productos': productos_aleatorios,
        'nombre_usuario': nombre_usuario,
        'is_home': True
    }
    return render(request, 'inicio.html', context)

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Autentica al usuario con el nombre de usuario y la contraseña proporcionados
            user = form.get_user()
            if user is not None:
                # Verificar si el usuario ya tiene una sesión activa
                if user.session_key:
                    try:
                        # Cerrar la sesión activa anterior
                        old_session = Session.objects.get(session_key=user.session_key)
                        old_session.delete()
                    except Session.DoesNotExist:
                        pass

                # Iniciar la nueva sesión para el usuario
                auth_login(request, user)

                # Guardar la nueva session_key en el usuario
                user.session_key = request.session.session_key
                user.save()

                # Redirigir al usuario a la página de inicio
                return redirect('inicio')

        error_message = "Nombre de usuario o contraseña incorrectos."
    else:
        form = LoginForm()
        error_message = None

    # Renderiza la plantilla 'login.html' pasando el formulario y el mensaje de error como contexto
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def logoutView (request):
    logout(request)
    return redirect('inicio')



class ProductUpdateView(LoginRequiredMixin, TenderoRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductForm
    template_name = 'productUpdate.html'
    success_url = reverse_lazy('listar_producto')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Obtener la cantidad de inventario del formulario
        cantidad_inventario = form.cleaned_data['cantidad_inventario']

        # Encontrar la entrada de inventario para el producto actualizado
        inventario = Inventario.objects.filter(id_producto=self.object).first()
        if inventario:
            # Actualizar la cantidad en el inventario
            inventario.cantidad = cantidad_inventario
            inventario.fecha_modificado = self.object.fecha_modificado
            inventario.id_usuario_modificacion = self.request.user
            inventario.save()
        else:
            # Si no hay una entrada en el inventario, puedes decidir qué hacer
            tienda = Tienda.objects.filter(id_usuario=self.request.user).first()
            if tienda:
                Inventario.objects.create(
                    id_tienda=tienda,
                    id_producto=self.object,
                    cantidad=cantidad_inventario,
                    id_usuario_creacion=self.request.user
                )
        return response



class ProductCreateView(TenderoRequiredMixin, CreateView):
    model = Producto
    form_class = ProductForm
    template_name = 'createProduct.html'
    success_url = reverse_lazy('listar_producto')

    def form_valid(self, form):
        # Asignar el usuario actual al producto
        form.instance.id_usuario_creacion = self.request.user
        response = super().form_valid(form)
        # Obtener la cantidad de inventario del formulario
        cantidad_inventario = form.cleaned_data['cantidad_inventario']
        # Seleccionar la primera tienda asociada al usuario actual
        tienda = Tienda.objects.filter(id_usuario=self.request.user).first()
        if not tienda:
            # Manejar el caso en el que no hay tiendas asociadas al usuario
            return HttpResponse('Usuario no asociado con una tienda')

        # Crear una entrada en el inventario para el nuevo producto
        Inventario.objects.create(
            id_tienda=tienda,
            id_producto=form.instance,
            cantidad=cantidad_inventario,
            id_usuario_creacion=self.request.user
        )

        return response

class ProductListView(ListView):
    model = Producto
    template_name = 'product_list.html'
    context_object_name = 'productos'  # Nombre del contexto para acceder a los productos en la plantilla
    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria_id = self.request.GET.get('categoria')  # Obtener el parámetro de categoría de la URL
        if categoria_id:
            queryset = queryset.filter(id_categoria_producto_id=categoria_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaProducto.objects.all()  # Pasar las categorías al contexto
        return context



class ProductDetailView(DetailView):
    model = Producto
    template_name = 'productDetail.html'


class ProductDeleteView(LoginRequiredMixin, TenderoRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productDelete.html'
    success_url = reverse_lazy('listar_producto')



class TiendaCreateView(LoginRequiredMixin, TenderoRequiredMixin, CreateView):
    model = Tienda
    form_class = TiendaForm
    template_name = 'tiendaCreate.html'
    success_url = reverse_lazy('listar_tienda')

    def form_valid(self, form):
        form.instance.id_usuario = self.request.user  # Asigna el usuario actual como gestor de la tienda
        return super().form_valid(form)

class TiendaListView(ListView):
    model = Tienda
    template_name = 'tiendaList.html'  # El nombre del template que se utilizará para renderizar la vista
    context_object_name = 'tiendas'  # Nombre de la variable de contexto en el template

    def get_queryset(self):
        # Puedes personalizar la consulta si es necesario
        return Tienda.objects.all()

class TiendaDetailView(DetailView):
    model = Tienda
    template_name = 'tiendaDetail.html'
    context_object_name = 'tienda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # El **kwargs lo usamos para traer el id de la tienda que seleccionemos
        print("kwargs:", kwargs) #es una prueba para ver que tienda seleccionamos en la terminal
        tienda = self.object
        context['tienda_id'] = tienda.id_tienda  # Agregar el ID de la tienda al contexto
        # Obtener los inventarios de la tienda
        inventarios = Inventario.objects.filter(id_tienda=tienda)
        context['inventarios'] = inventarios
        # Obtener productos de los inventarios de la tienda
        productos = Producto.objects.filter(inventario__id_tienda=tienda).distinct()
        context['productos'] = productos
        return context


class TiendaUpdateView(LoginRequiredMixin, TenderoRequiredMixin, UpdateView):
    model = Tienda
    form_class = TiendaForm
    template_name = 'tiendaUpdate.html'
    success_url = reverse_lazy('listar_tienda')

    def form_valid(self, form):
        # Puedes realizar acciones adicionales aquí si es necesario
        return super().form_valid(form)

class TiendaDeleteView(LoginRequiredMixin, TenderoRequiredMixin, DeleteView):
    model = Tienda
    template_name = 'tiendaDelete.html'
    success_url = reverse_lazy('listar_tienda')


class InventarioCreateView(TenderoRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'inventarioForm.html'
    def get_success_url(self):
        tienda_id = self.kwargs.get('tienda_id')
        return reverse('listar_inventario', kwargs={'tienda_id': tienda_id})

    def form_valid(self, form):
        tienda_id = self.kwargs.get('tienda_id')
        form.instance.id_tienda = get_object_or_404(Tienda, id_tienda=tienda_id)
        form.instance.id_usuario_creacion = self.request.user
        return super().form_valid(form)


class InventarioListView(ListView):
    model = Inventario
    template_name = 'inventarioList.html'
    context_object_name = 'inventarios'

    def get_queryset(self):
        tienda_id = self.kwargs.get('tienda_id')
        return Inventario.objects.filter(id_tienda=tienda_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tienda_id = self.kwargs.get('tienda_id')
        context['tienda'] = get_object_or_404(Tienda, id_tienda=tienda_id)
        return context


class InventarioUpdateView(UserPassesTestMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'inventarioUpdate.html'
    success_url = reverse_lazy('inventarioList')

    def test_func(self):
        inventario = self.get_object()
        try:
            tienda = Tienda.objects.get(id=self.get_object().id_tienda.id)
            return tienda.id_usuario == self.request.user
        except Tienda.DoesNotExist:
            return False

    def form_valid(self, form):
        form.instance.id_usuario_modificacion = self.request.user
        return super().form_valid(form)


class InventarioDeleteView(UserPassesTestMixin, DeleteView):
    model = Inventario
    template_name = 'inventarioDelete.html'
    success_url = reverse_lazy('listar_inventario')

    def test_func(self):
        inventario = self.get_object()
        try:
            tienda = Tienda.objects.get(id=inventario.id_tienda.id)
            return tienda.id_usuario == self.request.user
        except Tienda.DoesNotExist:
            return False

def agregar_producto(request, producto_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        producto = get_object_or_404(Producto, id_producto=producto_id)  # Cambiado de id a id_producto
        usuario = request.user

        # Verifica si ya hay un carrito activo para el usuario
        carrito, created = Carrito.objects.get_or_create(
            id_usuario=usuario,
            id_producto=producto,
            estado_carrito='activo',
            defaults={'fecha_creacion': date.today()}
        )

        # Si el carrito ya existe, simplemente lo utilizamos; de lo contrario, lo creamos
        if not created:
            carrito.deleted = False
            carrito.save()

        # Redirigir al carrito o a la misma página después de agregar
        return HttpResponseRedirect(reverse('carrito'))  # Ajusta según tu URL para la vista del carrito

    # Si no es un método POST, redirige a una página o muestra un error
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def CarritoView(request):
    usuario = request.user
    carrito_items = Carrito.objects.filter(id_usuario=usuario, estado_carrito='activo', deleted=False)
    total_precio = sum(item.id_producto.precio for item in carrito_items)
    context = {
        'carrito_items': carrito_items,
        'total_precio': total_precio

    }
    return render(request, 'carrito.html', context)



class CarritoDeleteView(DeleteView):
    model = Carrito
    template_name = 'carritoDelete.html'
    success_url = reverse_lazy('carrito')

    def get_queryset(self):
        return Carrito.objects.filter(id_usuario=self.request.user, estado_carrito='activo', deleted=False)


class SolicitudCreateView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudCreate.html'

    def form_valid(self, form):
        tienda_id = self.kwargs.get('tienda_id')  # Captura el 'tienda_id' desde la URL
        tienda = get_object_or_404(Tienda, id_tienda=tienda_id)  # Obtiene la tienda correspondiente
        form.instance.id_tienda = tienda  # Asigna la tienda al formulario

        # Asignar el usuario autenticado al campo 'id_usuario_creacion'
        form.instance.id_usuario_creacion = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detalle_tienda', kwargs={'pk': self.object.id_tienda.id_tienda})

class ListarSolicitudView(ListView):
    model = Solicitud
    template_name = 'solicitudList.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        # Filtra las solicitudes por la tienda específica
        tienda_id = self.kwargs.get('tienda_id')
        return Solicitud.objects.filter(id_tienda=tienda_id)

class ReseñaCreateView(CreateView):
    model = Reseña
    form_class = ReseñaForm
    template_name = 'reseñaCreate.html'

    def form_valid(self, form):
        tienda_id = self.kwargs.get('tienda_id')  # Captura el 'tienda_id' desde la URL
        tienda = get_object_or_404(Tienda, id_tienda=tienda_id)  # Obtiene la tienda correspondiente
        form.instance.id_tienda = tienda  # Asigna la tienda al formulario

        # Asignar el usuario autenticado al campo 'id_usuario_creacion'
        form.instance.id_usuario_creacion = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tienda_id = self.kwargs.get('tienda_id')  # Captura el 'tienda_id' desde la URL
        tienda = get_object_or_404(Tienda, id_tienda=tienda_id)  # Obtiene la tienda correspondiente
        context['tienda'] = tienda  # Incluye la tienda en el contexto
        return context

    def get_success_url(self):
        return reverse_lazy('detalle_tienda', kwargs={'pk': self.object.id_tienda.id_tienda})

def AboutView(request):
    if request.user.is_authenticated:
        nombre_usuario = request.user.username
    else:
        nombre_usuario = "invitado"

    about_content = {
        'aboutkey':"OnlineCommerce es la coneccion de todos los tenderos de barrio con sus vecinos",
        'nombre_usuario' : nombre_usuario,
    }

    return render(request, 'about.html', about_content)


def exportar_inventario(request, tienda_id):
    tienda = get_object_or_404(Tienda, id_tienda=tienda_id)

    # Verificar si el usuario tiene permiso para exportar
    if request.user.is_authenticated and (request.user == tienda.id_usuario or request.user.username == "sebastian"):
        inventarios = Inventario.objects.filter(id_tienda=tienda)

        # Crear la respuesta con el tipo de contenido para CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="inventario_{tienda.nombre}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Producto', 'Cantidad', 'Fecha de Creación'])

        # Escribir los datos del inventario
        for inventario in inventarios:
            writer.writerow([inventario.id_producto.nombre_producto, inventario.cantidad, inventario.fecha_creacion])

        return response
    else:
        return HttpResponse("No tienes permiso para exportar este inventario.", status=403)




