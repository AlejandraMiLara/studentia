from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import datetime
from .forms import RegistroUsuarioForm, EditarPerfilForm, ConfsPerfilForm, CursoForm, InscripcionCursoForm
from .models import ConfiguracionUsuario, Curso, AlumnoCurso
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string

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


            backend = get_backends()[0] 
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user) 

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

def generar_codigo():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Curso.objects.filter(codigo_acceso=codigo).exists():
            return codigo

@login_required
def crear_curso(request):
    if request.user.rol != 'Profesor': 
        messages.error(request, "No tienes permiso para crear cursos.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.id_profesor = request.user 
            curso.codigo_acceso = generar_codigo()
            curso.save()
            messages.success(request, "Curso creado con éxito.")
            return redirect('dashboard')

    else:
        form = CursoForm()

    return render(request, 'crear_curso.html', {'form': form})

@login_required
def inscribirse_curso(request):
    if request.method == "POST":
        form = InscripcionCursoForm(request.POST)
        if form.is_valid():
            codigo_acceso = form.cleaned_data["codigo_acceso"]

            curso = Curso.objects.filter(codigo_acceso=codigo_acceso).first()

            if not curso:
                messages.error(request, "El curso no existe.")
                return redirect("inscribirse_curso")

            if curso.id_profesor == request.user:
                messages.error(request, "No puedes inscribirte en tu propio curso.")
                return redirect("inscribirse_curso")

            if AlumnoCurso.objects.filter(curso=curso, alumno=request.user).exists():
                messages.error(request, "Ya estás inscrito en este curso.")
            else:
                AlumnoCurso.objects.create(curso=curso, alumno=request.user)
                #messages.success(request, f"Te has inscrito en {curso.nombre_curso} correctamente.")

            return redirect("dashboard")

    else:
        form = InscripcionCursoForm()

    return render(request, "inscribirse_curso.html", {"form": form})


@login_required
def dashboard(request):
    usuario = request.user
    es_profesor = usuario.rol == "Profesor"
    if es_profesor:
        cursos_creados = Curso.objects.filter(id_profesor=usuario) 
    else:
        cursos_creados = None

    cursos_inscritos = AlumnoCurso.objects.filter(alumno=usuario) 

    return render(request, "dashboard.html", {
        "es_profesor": es_profesor,
        "cursos_creados": cursos_creados,
        "cursos_inscritos": cursos_inscritos
    })

@login_required
def board(request, codigo_acceso):
    curso = get_object_or_404(Curso, codigo_acceso=codigo_acceso)

    return render(request, 'board.html',{
        'curso':curso
    })

def board_leave(request, codigo_acceso):
    usuario = request.user
    curso = get_object_or_404(Curso, codigo_acceso=codigo_acceso)

    inscripcion = get_object_or_404(AlumnoCurso, alumno=usuario, curso=curso)

    if request.method == "POST":
        inscripcion.delete()
        return redirect('dashboard')
    
    return render(request, 'board_leave.html', {
        "curso":curso
    })

@login_required
def board_borrar(request, codigo_acceso):
    curso = get_object_or_404(Curso, codigo_acceso=codigo_acceso)
    if request.method == "POST":
        curso.delete()
        return redirect('dashboard')
    return render(request, 'board_borrar.html', {'curso':curso})

@login_required
def board_actualizar(request, codigo_acceso):
    curso = get_object_or_404(Curso, codigo_acceso=codigo_acceso)

    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CursoForm(instance=curso)
    
    return render(request, 'board_actualizar.html', {
        'form':form, 'curso':curso
    })

@login_required
def board_add_activity(request, codigo_acceso):
    pass

@login_required
def board_add_content(request, codigo_acceso):
    curso = get_object_or_404(Curso, codigo_acceso=codigo_acceso)

    return render(request, 'board_add_content.html', {
        'curso':curso
    })

@login_required
def board_view_students(request, codigo_acceso):
    curso = get_object_or_404(Curso, codigo_acceso=codigo_acceso)
    alumnos_inscritos = AlumnoCurso.objects.filter(curso=curso).select_related('alumno')

    return render(request, 'board_view_students.html', {
        'curso':curso,
        'alumnos_inscritos':alumnos_inscritos
    })