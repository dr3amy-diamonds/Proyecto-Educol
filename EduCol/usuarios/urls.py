# usuarios/urls.py
from django.urls import path
from . import views
from .views import eventos_json
from django.contrib.auth import views as auth_views
from .views import (
    CursoListView, CursoDetailView, CursoCreateView,
    CursoUpdateView, CursoDeleteView
)

urlpatterns = [
    
    # Mis vistas

    path('login/',      views.login_view,   name='login'),
    path('registro/',   views.registro,     name='registro'),
    path('inicio/',     views.inicio,       name='inicio'),
    path('logout/',     views.logout_view,  name='logout'),
    path('biblioteca/', views.biblioteca,   name='biblioteca'),
    path('profesor/',   views.profesor,     name='profesor'),
    path('portafolio/', views.portafolio,   name='portafolio'),
    path('actividades/',views.actividades,  name='actividades'),
    path('bola/',       views.bola,         name='bola'),
    path('progreso/',   views.progreso,     name='progreso'),
    path('calendario/', views.calendario,   name='calendario'),
    path('noticias/',   views.noticias,     name='noticias'),
    path('compartir/',  views.compartir,    name='compartir'),
    path('guias/',      views.guias,        name='guias'),
    path('video_tutoriales/', views.video_tutoriales, name='video_tutoriales'),
    path('ejercicios/', views.ejercicios,   name='ejercicios'),
    path('retos/',      views.retos,        name='retos'),
    path('panel_profesor/',      views.panel_profesor,      name='panel_profesor'),
    path('perfil_editar/', views.perfil_editar, name='perfil_editar'),


    #Manejo de Actividades
   


    # Manejo de profesor
    
    path('formulario_profesor/',   views.formulario_profesor,     name='formulario_profesor'),

    # CRUD de Cursos

    path('cursos/',                     CursoListView.as_view(),    name='curso_list'),
    path('cursos/nuevo/',               CursoCreateView.as_view(),  name='curso_create'),
    path('cursos/<int:pk>/',            CursoDetailView.as_view(),  name='curso_detail'),
    path('cursos/<int:pk>/editar/',     CursoUpdateView.as_view(),  name='curso_update'),
    path('cursos/<int:pk>/eliminar/',   CursoDeleteView.as_view(),  name='curso_delete'),

    # Calendario

    path('api/eventos/', eventos_json, name='eventos_json'),

    # → Flujo de recuperación de contraseña
    # 1) Formulario r email
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),

    # 2) Página “email enviado”
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # 3) Link qde email: confirmar token y cambiar contraseña
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # 4) Página final “tu contraseña ha sido cambiada”
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]

