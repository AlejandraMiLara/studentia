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
    path('profile/settings', views.confs_perfil, name='confs_perfil'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new/course', views.crear_curso, name='crear_curso'),
    path("course/join", views.inscribirse_curso, name="inscribirse_curso"),
    path("board/<str:codigo_acceso>", views.board, name="board"),
    path("board/<str:codigo_acceso>/delete", views.board_borrar, name="board_borrar"),
    path("board/<str:codigo_acceso>/update", views.board_actualizar, name="board_actualizar"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)