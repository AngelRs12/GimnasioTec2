from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'gym/index.html')

def usuarios(request):
    return render(request, 'gym/usuarios.html')

def entradas_salidas(request):
    return render(request, 'gym/entradas_salidas.html')

def reportes(request):
    return render(request, 'gym/reportes.html')

def membresias(request):
    return render(request, 'gym/membresias.html')

def observaciones(request):
    return render(request, 'gym/observaciones.html')

def gestion_usuarios(request):
    if request.method == "POST":
        accion = request.POST.get("accion")
        tipo_usuario = request.POST.get("tipo_usuario")
        nombre = request.POST.get("nombre")
        apellido_paterno = request.POST.get("apellido_paterno")
        apellido_materno = request.POST.get("apellido_materno")
        correo = request.POST.get("correo")  # si aplica
        no_control = request.POST.get("no_control")  # si aplica

        # Solo ejecutamos si es "agregar"
        if accion == "agregar":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""CALL insertar_usuario_general(%s, %s, %s, %s, %s, %s)""", 
                    [nombre, 
                    apellido_paterno, 
                    apellido_materno, 
                    tipo_usuario, 
                    no_control, 
                    correo
                    ])
                print("SP ejecutado correctamente")
            except Exception as e:
                print("Error:", e)
    return render(request, 'gym/usuarios.html')
  