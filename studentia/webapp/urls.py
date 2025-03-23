from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.iniciar_sesion, name="iniciar_sesion"),
    path('signup/', views.registrar_usuario, name="registrar_usuario"),
    path('logout/', views.salir, name='salir'),
    path('profile/', views.ver_perfil, name='ver_perfil'),
    path('profile/edit', views.editar_perfil, name='editar_perfil'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)