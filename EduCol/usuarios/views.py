from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
from .models import Curso, Modulo, Actividad

from .models import Libro  # Asegúrate de tener esto

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=correo, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')

def inicio(request):
    """
    Vista para la página de inicio (dashboard).
    El template recibirá 'is_profesor' para decidir a dónde lleva el botón.
    """
    # Asumimos usuario anónimo => no profesor
    is_profesor = False
    if request.user.is_authenticated:
        # Comprueba si pertenece al grupo 'Profesores'
        is_profesor = request.user.groups.filter(name='Profesores').exists()
    return render(request, 'usuarios/inicio.html', {
        'is_profesor': is_profesor
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def biblioteca(request):
    area_sel = request.GET.get('area')  # Área seleccionada desde la URL
    areas = [area for area, _ in Libro.AREAS]  # Lista de áreas definidas en el modelo
    libros = Libro.objects.filter(area=area_sel) if area_sel else []  # Libros filtrados por área
    context = {
        'areas': areas,
        'area_sel': area_sel,
        'libros': libros
    }
    return render(request, 'usuarios/biblioteca.html', context)

@login_required(login_url='login')
def profesor(request):
    return render(request, 'usuarios/profesor.html')

@login_required(login_url='login')
def portafolio(request):
    return render(request, 'usuarios/portafolio.html')

@login_required(login_url='login')
def actividades(request):
    return render(request, 'usuarios/actividades.html')

def bola(request):
    is_profesor = False
    if request.user.is_authenticated:
        is_profesor = request.user.groups.filter(name='Profesores').exists()
    return render(request, 'usuarios/bola.html', {
        'is_profesor': is_profesor
    })

@login_required(login_url='login')
def progreso(request):
    return render(request, 'usuarios/progreso.html')

@login_required(login_url='login')
def compartir(request):
    return render(request, 'usuarios/compartir.html')

@login_required(login_url='formulario_profesor')
def formulario_profesor(request):
    return render(request, 'usuarios/formulario_profesor.html')

@login_required(login_url='login')
def calendario(request):
    return render(request, 'usuarios/calendario.html')

@login_required(login_url='login')
def noticias(request):
    return render(request, 'usuarios/noticias.html')

@login_required(login_url='login')
def guias(request):
    return render(request, 'usuarios/guias.html')

@login_required(login_url='login')
def video_tutoriales(request):
    return render(request, 'usuarios/video_tutoriales.html')

@login_required(login_url='login')
def ejercicios(request):
    return render(request, 'usuarios/ejercicios.html')

@login_required(login_url='login')
def retos(request):
    return render(request, 'usuarios/retos.html')




def eventos_json(request):
    eventos = []

    # 1) Cada Curso como evento de rango completo
    for c in Curso.objects.all():
        eventos.append({
            'title': c.nombre,
            'start': c.inicio.isoformat(),
            'end':   (c.fin + timedelta(days=1)).isoformat(),
            'color': '#345ab2'
        })

    # 2) Cada Módulo como sub-rango dentro del curso
    for m in Modulo.objects.select_related('curso'):
        eventos.append({
            'title': f"{m.curso.nombre} · {m.titulo}",
            'start': m.inicio.isoformat(),
            'end':   (m.fin + timedelta(days=1)).isoformat(),
            'color': '#12b334'
        })

    # 3) Cada Actividad como punto en el tiempo
    for a in Actividad.objects.select_related('modulo'):
        eventos.append({
            'title': a.titulo,
            'start': a.fecha_entrega.isoformat(),
            'allDay': True,
            'color': '#b22222'
        })

    return JsonResponse(eventos, safe=False)

# usuarios/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Curso

# 1) Listado de cursos de un profesor
class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'usuarios/curso_list.html'  # tu plantilla
    context_object_name = 'cursos'

    def get_queryset(self):
        # Solo los cursos que crea el profesor actual
        return Curso.objects.filter(profesor=self.request.user)

# 2) Ver detalle de un curso
class CursoDetailView(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = 'usuarios/curso_detail.html'
    context_object_name = 'curso'

# 3) Crear un curso (solo para profesores)
class CursoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'inicio', 'fin']
    template_name = 'usuarios/curso_form.html'
    permission_required = 'usuarios.add_curso'
    # Tras crear, redirige al listado
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        # Asigna automáticamente al profesor actual
        form.instance.profesor = self.request.user
        return super().form_valid(form)

# 4) Editar un curso
class CursoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Curso
    fields = ['nombre', 'descripcion', 'inicio', 'fin']
    template_name = 'usuarios/curso_form.html'
    permission_required = 'usuarios.change_curso'
    success_url = reverse_lazy('curso_list')

# 5) Borrar un curso
class CursoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Curso
    template_name = 'usuarios/curso_confirm_delete.html'
    permission_required = 'usuarios.delete_curso'
    success_url = reverse_lazy('curso_list')

from django.shortcuts      import render, redirect
from django.contrib        import messages
from django.contrib.auth   import get_user_model
from django.contrib.auth.models import Group
from .forms                import ProfesorRegisterForm
from .models               import ProfesorProfile

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import ProfesorRegisterForm
from .models import ProfesorProfile, Usuario

def formulario_profesor(request):
    if request.method == 'POST':
        form = ProfesorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # 1) Creas el usuario
            user = Usuario.objects.create_user(
                mail=form.cleaned_data['mail'],
                password=form.cleaned_data['password1'],
                nombre_completo=form.cleaned_data['nombre_completo']
            )
            # 2) Creamos el perfil
            perfil = ProfesorProfile.objects.create(
                user            = user,
                nivel_educativo = form.cleaned_data['nivel_educativo'],
                # ... resto de campos ...
                especialidades  = form.cleaned_data['especialidades']
            )
            # 3) Lo metemos al grupo Profesores
            grupo = Group.objects.get(name='Profesores')
            user.groups.add(grupo)

            # 4) Logeamos al usuario (opcionales)
            login(request, user)
            return redirect('panel_profesor')
    else:
        form = ProfesorRegisterForm()
    return render(request, 'usuarios/formulario_profesor.html', {'form': form})

def perfil(request):
    # Comprueba si el usuario pertenece al grupo "Profesores"
    es_profesor = request.user.groups.filter(name='Profesores').exists()
    return render(request, 'usuarios/perfil.html', {
        'es_profesor': es_profesor,
    })

@login_required
def panel_profesor(request):
    # Obtenemos todos los usuarios del grupo Profesores
    grupo  = Group.objects.get(name='Profesores')
    profs = grupo.usuarios_groups.all()
    return render(request, 'usuarios/panel_profesor.html', {
        'profesores': profs
    })

@login_required
def perfil_editar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pw1   = request.POST.get('password1')
        pw2   = request.POST.get('password2')

        if pw1 and pw1 != pw2:
            messages.error(request, "Las contraseñas no coinciden.")
        else:
            user = request.user
            user.email = email
            if pw1:
                user.set_password(pw1)
            user.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')

    return redirect('perfil')  # o podrías volver a mostrar un form con errores






