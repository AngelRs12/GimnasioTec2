from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.http import JsonResponse
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

def reglamento(request):
    return render(request, 'gym/reglamento.html')

def horario(request):
    return render(request, 'gym/horario.html')

def entrenadores(request):
    return render(request, 'gym/entrenadores.html')

def actividades(request):
    return render(request, 'gym/actividades.html')

def acercade(request):
    return render(request, 'gym/acercade.html')

def gestion_usuarios(request):
    if request.method == "POST":
        accion = request.POST.get("accion")
        tipo_usuario = request.POST.get("tipo_usuario")
        nombre = request.POST.get("nombre")
        apellido_paterno = request.POST.get("apellido_paterno")
        apellido_materno = request.POST.get("apellido_materno")
        correo = request.POST.get("correo")  # si aplica
        no_control = request.POST.get("no_control")  # si aplica

        if accion == "agregar":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CALL insertar_usuario_general(%s, %s, %s, %s, %s, %s)
                    """, [
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        tipo_usuario,
                        no_control,
                        correo
                    ])
                print("SP ejecutado correctamente")

                # Si es una petición AJAX, devolver JSON
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": True})

                # Si no es AJAX, render normal
                return render(request, 'gym/usuarios.html', {"mensaje": "Usuario agregado correctamente."})

            except Exception as e:
                error_msg = str(e)
    # Si viene con "CONTEXT:", cortamos desde ahí
                if "CONTEXT:" in error_msg:
                    error_msg = error_msg.split("CONTEXT:")[0].strip()


                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "error": error_msg}, status=400)

                return render(request, 'gym/usuarios.html', {"error": error_msg})
 # === BUSCAR USUARIO === (AJAX con fetch)
    elif request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        id_usuario = request.GET.get("id_usuario", "").strip()
        nombre = request.GET.get("nombre", "").strip()
        print("SP ejecutado correctamente1")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM buscar_usuario(%s, %s)", [id_usuario, nombre])
                columnas = [col[0] for col in cursor.description]
                resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
                print("SP ejecutado correctamente22222")
            return JsonResponse({"success": True, "resultados": resultados})

        except Exception as e:
            error_str = str(e).split("CONTEXT:")[0].strip()
            print("SP ejecutado correctamente2")
            return JsonResponse({"success": False, "error": error_str}, status=400)

    # Render inicial (vista HTML normal)
    return render(request, "gym/usuarios.html")

  