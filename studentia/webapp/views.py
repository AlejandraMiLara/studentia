from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import datetime
from .forms import RegistroUsuarioForm, EditarPerfilForm, ConfsPerfilForm
from .models import ConfiguracionUsuario
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def salir(request):
    logout(request)
    return redirect('inicio')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'iniciar_sesion.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Asignar backend explícitamente
            backend = get_backends()[0]  # Primer backend de la lista
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)  # Loguea automáticamente después de registrarse

            return redirect('inicio')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registrar_usuario.html', {'form': form})

@login_required
def ver_perfil(request):
    return render(request, 'perfil.html', {'usuario':request.user})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})

@login_required
def confs_perfil(request):
    configuracion = get_object_or_404(ConfiguracionUsuario, usuario=request.user)

    if request.method == 'POST':
        form = ConfsPerfilForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guardado!')
            return redirect('ver_perfil')
    else:
        form = ConfsPerfilForm(instance=configuracion)

    return render(request, 'confs_perfil.html', {'form': form})