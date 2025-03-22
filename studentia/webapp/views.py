from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .forms import RegistroUsuarioForm
from django.contrib.auth import authenticate, login, logout
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
            login(request, user)  # Loguea automáticamente después de registrarse
            return redirect('inicio')  # Cambia 'inicio' por tu ruta principal
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registrar_usuario.html', {'form': form})