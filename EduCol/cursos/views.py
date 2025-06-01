from django.shortcuts import render
from .models import Curso

def lista_cursos(request):
    # Consulta todos los cursos de la base de datos.
    cursos = Curso.objects.all()
    # Renderiza la plantilla 'lista_cursos.html' pasándole los cursos.
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})
