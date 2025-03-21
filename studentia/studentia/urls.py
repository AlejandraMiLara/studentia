
from django.contrib import admin
from django.urls import path
from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('login', views.iniciar_sesion, name="iniciar_sesion"),
    path('signup', views.registrar_usuario, name="registrar_usuario"),
]
