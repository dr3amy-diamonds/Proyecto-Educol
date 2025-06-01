# educol/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # redirige la raíz al login
    path('', lambda req: redirect('login'), name='home'),

    # admin (solo en /admin/)
    path('admin/', admin.site.urls),

    # TODAS las vistas de auth y tus propias vistas de usuarios
    # se definen en usuarios/urls.py, así que aquí solo incluyes esa app:
    path('', include('usuarios.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)