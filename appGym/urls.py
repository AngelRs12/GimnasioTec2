from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('reportes/', views.reportes, name='reportes'),
    path('membresias/', views.membresias, name='membresias'),
    path('observaciones/', views.observaciones, name='observaciones'),
    path('entradas_salidas/', views.entradas_salidas, name='entradas_salidas'),
    path('reglamento/', views.reglamento, name='reglamento'),
    path('horario/', views.horario, name='horario'),
    path('actividades/', views.actividades, name='actividades'),
    path('entrenadores/', views.entrenadores, name='entrenadores'),
    path('acercade/', views.acercade, name='acercade'),
    path('gestion_usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('sesion/', views.sesion, name='sesion'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("registrar_ingreso/", views.registrar_ingreso, name="registrar_ingreso"),
    path("guardar_observacion/", views.guardar_observacion, name="guardar_observacion"),
    path("listar_observaciones/", views.listar_observaciones, name="listar_observaciones"),
    path('editar_observacion/', views.editar_observacion_view, name='editar_observacion'),
    path('eliminar_observacion/', views.eliminar_observacion_view, name='eliminar_observacion'),
    path("eliminar_usuario/", views.eliminar_usuario, name="eliminar_usuario"),
    path('administradores/', views.administradores, name='administradores'),
    path('crear_admin/', views.crear_admin, name='crear_admin'),
    path('buscar_admin/', views.buscar_admin, name='buscar_admin'),
    path('eliminar_admin/', views.eliminar_admin, name='eliminar_admin'),
    path('editar_admin/', views.editar_admin, name='editar_admin'),
    path("crear_membresia/", views.crear_membresia, name="crear_membresia"),
    path("obtener_membresias/", views.obtener_membresias, name="obtener_membresias"),
    path("editar_membresia/", views.editar_membresia, name="editar_membresia"),
    path("eliminar_membresia/", views.eliminar_membresia, name="eliminar_membresia"),
    path('reportes/data/', views.reportes_data, name='reportes_data'),  # opcional, para AJAX
    
    
    path('reportes/excel/', views.generar_reporte_excel, name='generar_reporte_excel'),
    
    
    path('actividades/agregar/', views.actividad_agregar, name='actividad_agregar'),
    path('actividades/editar/<int:id_actividad>/', views.actividad_editar, name='actividad_editar'),
    path('actividades/eliminar/<int:id_actividad>/', views.actividad_eliminar, name='actividad_eliminar'),
    path('actividades_json/', views.actividades_json, name='actividades_json'),
    path('editar_entrenador/<int:id_entrenador>/', views.editar_entrenador, name='editar_entrenador'),
    path('agregar_entrenador/', views.agregar_entrenador, name='agregar_entrenador'),
    path('entrenadores/eliminar/<int:id_entrenador>/', views.eliminar_entrenador, name='eliminar_entrenador'), 
    path('lista_entrenadores_json/', views.lista_entrenadores_json, name='lista_entrenadores_json'),
    
    
    
    path('reportes/uso-gimnasio/', views.uso_gimnasio_data, name='uso_gimnasio_data'),


]