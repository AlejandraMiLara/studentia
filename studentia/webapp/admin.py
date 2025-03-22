from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado, ConfiguracionUsuario, Curso, ConfiguracionCurso, AlumnoCurso, Reporte, Actividad, Envio


# Register your models here.

class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    list_display = ['username', 'email', 'rol', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'sobre_mi', 'foto_perfil')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol', 'sobre_mi', 'foto_perfil')}),
    )

class ConfiguracionUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'recibir_notificaciones', 'recibir_ofertas')
    search_fields = ('usuario__username',)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre_curso', 'id_profesor', 'codigo_acceso', 'descripcion')
    search_fields = ('nombre_curso', 'id_profesor__username', 'codigo_acceso')

class ConfiguracionCursoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'estado')
    search_fields = ('curso__nombre_curso',)

class AlumnoCursoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'alumno')
    search_fields = ('curso__nombre_curso', 'alumno__username')

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('reportante', 'reportado', 'curso', 'motivo')
    search_fields = ('reportante__username', 'reportado__username', 'curso__nombre_curso')

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'fecha', 'docente', 'generado_por_ia')
    search_fields = ('titulo', 'curso__nombre_curso', 'docente__username')

class EnvioAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'docente', 'actividad', 'curso', 'fecha', 'calificacion')
    search_fields = ('alumno__username', 'docente__username', 'actividad__titulo', 'curso__nombre_curso')


admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)
admin.site.register(ConfiguracionUsuario, ConfiguracionUsuarioAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(ConfiguracionCurso, ConfiguracionCursoAdmin)
admin.site.register(AlumnoCurso, AlumnoCursoAdmin)
admin.site.register(Reporte, ReporteAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(Envio, EnvioAdmin)