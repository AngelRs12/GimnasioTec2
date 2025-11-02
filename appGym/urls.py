from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('reportes/', views.reportes, name='reportes'),
    path('membresias/', views.membresias, name='membresias'),
    path('observaciones/', views.observaciones, name='observaciones'),
    path('entradas_salidas/', views.entradas_salidas, name='entradas_salidas'),
    
    path('gestion_usuarios/', views.gestion_usuarios, name='gestion_usuarios')
]