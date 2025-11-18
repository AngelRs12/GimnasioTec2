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

def sesion(request):
    return render(request, 'gym/sesion.html')

def login(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT validar_usuario_admin(%s, %s);",
                [usuario, password]
            )
            resultado = cursor.fetchone()[0]  # True o False

        if resultado:  # Si las credenciales son correctas
            request.session["usuario_admin"] = usuario
            return redirect("index")  # Ajusta a tu vista principal

        else:  # Credenciales incorrectas
            return render(request, 'gym/sesion.html', {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "index.html")

def logout(request):
    request.session.flush()
    return redirect("index")  # Ajusta a tu vista principal

#Backend

def crear_usuario(request):   
    return render(request, 'gym/crear_usuario.html')

def crear_usuario_admin(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO public."Usuarios_admin" ("Usuario", "Password") VALUES (%s, %s);',
                [usuario, password]
            )

        # Ajusta a la vista a la que quieras regresar
    return render(request, "gym/crear_usuario.html")





def gestion_usuarios(request):
    if request.method == "POST":
        accion = request.POST.get("accion")
        tipo_usuario = request.POST.get("tipo_usuario")
        nombre = request.POST.get("nombre")
        apellido_paterno = request.POST.get("apellido_paterno")
        apellido_materno = request.POST.get("apellido_materno")
        no_control = request.POST.get("no_control")  # si aplica
        equipo = request.POST.get("equipo")  # si aplica (solo representativo)

        if accion == "agregar":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT insertar_usuario_general(%s, %s, %s, %s, %s, %s)
                    """, [
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        tipo_usuario,
                        no_control,
                        equipo  # nuevo parámetro
                    ])

                    # Recuperar el id del usuario recién insertado
                    nuevo_id = cursor.fetchone()[0]

                    # Si es una petición AJAX, devolver JSON
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({
                        "success": True,
                        "mensaje": f"Usuario agregado correctamente (ID: {nuevo_id}).",
                    })

                    # Si no es AJAX, render normal
                    return render(
                        request,
                        "gym/usuarios.html",
                        {"mensaje": f"Usuario agregado correctamente (ID: {nuevo_id})."}
                    )

            except Exception as e:
                error_msg = str(e)


        if accion == "editar":
            id_usuario = request.POST.get("id_usuario")   # ← AQUI ES DONDE LO NECESITAS
            nombre = request.POST.get("nombre")
            apellido_paterno = request.POST.get("apellido_paterno")
            apellido_materno = request.POST.get("apellido_materno")
            tipo_usuario = request.POST.get("tipo_usuario")
            no_control = request.POST.get("no_control")
            equipo = request.POST.get("equipo")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT editar_usuario_general(%s, %s, %s, %s, %s, %s, %s)
                    """, [
                        id_usuario,
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        tipo_usuario,
                        no_control if no_control else None,
                        equipo if equipo else None
                    ])

                    mensaje = cursor.fetchone()[0]  # La función retorna texto

                    # Petición AJAX → JSON
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({
                            "success": True,
                            "mensaje": mensaje,
                            "id_usuario": id_usuario
                        })

                    # Petición normal → recarga de página
                    return render(
                        request,
                        "gym/usuarios.html",
                        {"mensaje": mensaje}
                    )

            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                })

        # Si viene con "CONTEXT:", cortamos desde ahí
        if "CONTEXT:" in error_msg:
            error_msg = error_msg.split("CONTEXT:")[0].strip()

        # Respuesta AJAX
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": error_msg}, status=400)

        # Respuesta normal
        return render(request, "gym/usuarios.html", {"error": error_msg})
    
 # === BUSCAR USUARIO === (AJAX con fetch)
    elif request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        id_usuario = request.GET.get("id_usuario", "").strip()
        nombre = request.GET.get("nombre", "").strip()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM buscar_usuario(%s, %s)", [id_usuario, nombre])
                columnas = [col[0] for col in cursor.description]
                resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
            return JsonResponse({"success": True, "resultados": resultados})

        except Exception as e:
            error_str = str(e).split("CONTEXT:")[0].strip()
            return JsonResponse({"success": False, "error": error_str}, status=400)

    # Render inicial (vista HTML normal)
    return render(request, "gym/usuarios.html")


def registrar_ingreso(request):
    if request.method == "POST":
        id_usuario = request.POST.get("id_usuario")
        tipo = request.POST.get("tipo")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT insertar_ingreso(%s, %s);",
                    [id_usuario, tipo]
                )
                mensaje = cursor.fetchone()[0]

            return JsonResponse({"success": True, "mensaje": mensaje})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})


def guardar_observacion(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha = request.POST.get("fecha_publicacion")

        if not titulo or not descripcion or not fecha:
            return JsonResponse({"success": False, "error": "Todos los campos son obligatorios."})

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT insertar_observacion(%s, %s, %s);",
                    [titulo, descripcion, fecha]
                )
                mensaje = cursor.fetchone()[0]

            return JsonResponse({"success": True, "mensaje": mensaje})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})


def listar_observaciones(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listar_observaciones();")
        rows = cursor.fetchall()

    columnas = ["id_observacion", "titulo", "descripcion", "fecha_publicacion"]
    data = [dict(zip(columnas, fila)) for fila in rows]

    return JsonResponse(data, safe=False)


def editar_observacion_view(request):
    if request.method == "POST":
        id_observacion = request.POST.get("id_observacion")
        descripcion = request.POST.get("descripcion")

        if not id_observacion or not descripcion:
            return JsonResponse({"success": False, "error": "ID y descripción son obligatorios."})

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT editar_observacion(%s, %s);",
                    [id_observacion, descripcion]
                )
                mensaje = cursor.fetchone()[0]

            return JsonResponse({"success": True, "mensaje": mensaje})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})

def eliminar_observacion_view(request):
    if request.method == "POST":
        id_observacion = request.POST.get("id_observacion")

        if not id_observacion:
            return JsonResponse({"success": False, "error": "ID es obligatorio."})

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT eliminar_observacion(%s);",
                    [id_observacion]
                )
                mensaje = cursor.fetchone()[0]

            return JsonResponse({"success": True, "mensaje": mensaje})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})

def eliminar_usuario(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        id_usuario = request.POST.get("id_usuario")
        if not id_usuario:
            return JsonResponse({"success": False, "error": "ID de usuario no proporcionado."})
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT public.eliminar_usuario(%s);", [int(id_usuario)])
            return JsonResponse({"success": True, "mensaje": f"Usuario {id_usuario} eliminado correctamente."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido."})