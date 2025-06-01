# usuarios/admin.py
from django.contrib import admin
from .models import Usuario
from .models import Libro
from .models import Usuario, Libro, Curso, Modulo, Actividad

admin.site.register(Usuario)

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'autor', 'area')
    list_filter   = ('area',)
    search_fields = ('titulo', 'autor')

# Modelos para gestionar cursos y calendario:

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'inicio', 'fin')
    list_filter  = ('profesor',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'inicio', 'fin')
    list_filter  = ('curso',)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'fecha_entrega')
    list_filter  = ('modulo',)
