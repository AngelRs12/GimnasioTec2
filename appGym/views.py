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

def administradores(request):   
    return render(request, 'gym/administradores.html')

def crear_admin(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO public."Usuarios_admin" ("Usuario", "Password") VALUES (%s, %s);',
                [usuario, password]
            )

        # Ajusta a la vista a la que quieras regresar
    return render(request, "gym/administradores.html")

def buscar_admin(request):
    """
    Busca administradores:
     - Si no hay parámetros GET renderiza administradores.html.
     - Parámetros aceptados (GET): id_admin (num) y usuario (texto).
     - Devuelve JSON cuando la petición es AJAX; si no, renderiza template con resultados en contexto.
    """
    id_param = (request.GET.get("id_admin") or request.GET.get("id")) and (request.GET.get("id_admin") or request.GET.get("id"))
    nombre = (request.GET.get("usuario") or request.GET.get("nombre") or "").strip()

    # Si no hay criterios -> render
    if not id_param and not nombre:
        return render(request, "gym/administradores.html")

    try:
        with connection.cursor() as cursor:
            if nombre:
                cursor.execute(
                    """
                    SELECT
                      row_number() OVER (ORDER BY "Usuario") AS id_admin,
                      "Usuario" AS usuario
                    FROM public."Usuarios_admin"
                    WHERE "Usuario" ILIKE %s
                    ORDER BY "Usuario"
                    LIMIT 200;
                    """,
                    [f"%{nombre}%"]
                )
                rows = cursor.fetchall()
            else:
                # búsqueda por id_admin: usamos row_number() para generar ids estables según orden alfabético
                try:
                    id_int = int(id_param)
                except Exception:
                    rows = []
                else:
                    cursor.execute(
                        """
                        SELECT id_admin, usuario FROM (
                          SELECT
                            row_number() OVER (ORDER BY "Usuario") AS id_admin,
                            "Usuario" AS usuario
                          FROM public."Usuarios_admin"
                          ORDER BY "Usuario"
                        ) t WHERE t.id_admin = %s LIMIT 1;
                        """,
                        [id_int]
                    )
                    rows = cursor.fetchall()

        resultados = [{"id_admin": r[0], "usuario": r[1]} for r in rows]

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "resultados": resultados})
        else:
            return render(request, "gym/administradores.html", {"resultados": resultados, "query_usuario": nombre, "query_id": id_param})

    except Exception as e:
        err = str(e)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": err}, status=500)
        return render({"error": f"No fue posible realizar la búsqueda: {err}"})


def eliminar_admin(request):
    """
    Elimina un administrador.
    - POST con 'usuario' o 'id_admin'.
    - Responde JSON si es AJAX, si no redirige/renderiza.
    """
    if request.method != "POST":
        return redirect("administradores")

    if "usuario_admin" not in request.session:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": "No autorizado"}, status=403)
        messages.error(request, "Debes iniciar sesión como administrador.")
        return redirect("sesion")

    usuario = (request.POST.get("usuario") or "").strip()
    id_param = request.POST.get("id_admin") or request.POST.get("id")

    try:
        with connection.cursor() as cursor:
            # Si nos dieron id_admin, resolvemos el usuario
            if id_param and not usuario:
                try:
                    id_int = int(id_param)
                except ValueError:
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({"success": False, "error": "ID inválido."}, status=400)
                    return render(request, "gym/administradores.html", {"error": "ID inválido."})

                cursor.execute(
                    """
                    SELECT usuario FROM (
                      SELECT row_number() OVER (ORDER BY "Usuario") AS id_admin,
                             "Usuario" AS usuario
                      FROM public."Usuarios_admin" ORDER BY "Usuario"
                    ) t WHERE t.id_admin = %s LIMIT 1;
                    """,
                    [id_int]
                )
                fila = cursor.fetchone()
                if not fila:
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({"success": False, "error": "Administrador no encontrado."}, status=404)
                    return render(request, "gym/administradores.html", {"error": "Administrador no encontrado."})
                usuario = fila[0]

            if not usuario:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "error": "Usuario a eliminar no proporcionado."}, status=400)
                return render(request, "gym/administradores.html", {"error": "Usuario a eliminar no proporcionado."})

            cursor.execute(
                'DELETE FROM public."Usuarios_admin" WHERE "Usuario" = %s;',
                [usuario]
            )
            if cursor.rowcount == 0:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "error": "Administrador no encontrado."}, status=404)
                return render(request, "gym/administradores.html", {"error": "Administrador no encontrado."})

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "mensaje": f"Administrador '{usuario}' eliminado correctamente."})
        messages.success(request, f"Administrador '{usuario}' eliminado correctamente.")
        return redirect("administradores")

    except Exception as e:
        err = str(e)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": err}, status=500)
        return render(request, "gym/administradores.html", {"error": f"No fue posible eliminar el administrador: {err}"})









def editar_admin(request):
    """
    Edita la información de un administrador.
    - Acepta POST con:
        - 'usuario' (nombre actual) o 'id_admin' (num) para identificar el registro
        - 'password' nueva (requerida)
    - Responde JSON si es AJAX, o redirige/renderiza otherwise.
    """
    if request.method != "POST":
        return redirect("administradores")

    if "usuario_admin" not in request.session:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": "No autorizado"}, status=403)
        messages.error(request, "Debes iniciar sesión como administrador.")
        return redirect("sesion")

    usuario = (request.POST.get("usuario") or "").strip()
    password = (request.POST.get("password") or "").strip()
    id_param = request.POST.get("id_admin") or request.POST.get("id")

    if not password:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": "La nueva contraseña es obligatoria."}, status=400)
        return render(request, "gym/administradores.html", {"error": "La nueva contraseña es obligatoria."})

    try:
        with connection.cursor() as cursor:
            # Si nos dieron id_admin, resolvemos el usuario correspondiente
            if id_param and not usuario:
                try:
                    id_int = int(id_param)
                except ValueError:
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({"success": False, "error": "ID inválido."}, status=400)
                    return render(request, "gym/administradores.html", {"error": "ID inválido."})

                cursor.execute(
                    """
                    SELECT usuario FROM (
                      SELECT row_number() OVER (ORDER BY "Usuario") AS id_admin,
                             "Usuario" AS usuario
                      FROM public."Usuarios_admin" ORDER BY "Usuario"
                    ) t WHERE t.id_admin = %s LIMIT 1;
                    """,
                    [id_int]
                )
                fila = cursor.fetchone()
                if not fila:
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse({"success": False, "error": "Administrador no encontrado."}, status=404)
                    return render(request, "gym/administradores.html", {"error": "Administrador no encontrado."})
                usuario = fila[0]

            if not usuario:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "error": "Usuario a editar no proporcionado."}, status=400)
                return render(request, "gym/administradores.html", {"error": "Usuario a editar no proporcionado."})

            # Actualizar contraseña
            cursor.execute(
                'UPDATE public."Usuarios_admin" SET "Password" = %s WHERE "Usuario" = %s;',
                [password, usuario]
            )
            if cursor.rowcount == 0:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "error": "Administrador no encontrado."}, status=404)
                return render(request, "gym/administradores.html", {"error": "Administrador no encontrado."})

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "mensaje": f"Contraseña de '{usuario}' actualizada correctamente."})
        messages.success(request, f"Contraseña de '{usuario}' actualizada correctamente.")
        return redirect("administradores")

    except Exception as e:
        err = str(e)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": err}, status=500)
        return render(request, "gym/administradores.html", {"error": f"No fue posible editar el administrador: {err}"})

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