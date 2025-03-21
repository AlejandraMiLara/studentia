from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def iniciar_sesion(request):
    return render(request, 'iniciar_sesion.html')

def registrar_usuario(request):
    return render(request, 'registrar_usuario.html')