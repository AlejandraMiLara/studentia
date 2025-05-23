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
    path('profile/view/<int:id>', views.other_profile, name='other_profile'),
    path('profile/edit', views.editar_perfil, name='editar_perfil'),
    path('profile/settings', views.confs_perfil, name='confs_perfil'),
    path('profile/', views.ver_perfil, name='ver_perfil'),
    path('report/student/<int:id>', views.report, name="report"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new/course', views.crear_curso, name='crear_curso'),
    path("course/join", views.inscribirse_curso, name="inscribirse_curso"),
    path("board/<str:codigo_acceso>", views.board, name="board"),
    path("board/<str:codigo_acceso>/leave", views.board_leave, name="board_leave"),
    path("board/<str:codigo_acceso>/delete", views.board_borrar, name="board_borrar"),
    path("board/<str:codigo_acceso>/update", views.board_actualizar, name="board_actualizar"),
    path("board/<str:codigo_acceso>/add/content", views.board_add_content, name="board_add_content"),
    path("board/<str:codigo_acceso>/view/students", views.board_view_students, name="board_view_students"),
    path("board/<str:codigo_acceso>/remove/<int:id_alumno>", views.board_remove_student, name="board_remove_student"),
    path("board/<str:codigo_acceso>/actividad/<int:id_actividad>/edit", views.content_edit, name="content_edit"),
    path("board/<str:codigo_acceso>/actividad/<int:id_actividad>/delete", views.content_delete, name="content_delete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)