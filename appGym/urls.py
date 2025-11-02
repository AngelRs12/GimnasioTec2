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
    path('acercade/', views.acercade, name='acercade')
   
]