import time
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_POST
import io
import base64
from django.http import HttpResponse
import os
from django.conf import settings
import uuid

def index(request):
    return render(request, 'gym/index.html')

def usuarios(request):
    return render(request, 'gym/usuarios.html')

def entradas_salidas(request):
    return render(request, 'gym/entradas_salidas.html')

def graficas(request):
    return render(request, 'gym/graficas.html')

def membresias(request):
    return render(request, 'gym/membresias.html')

def observaciones(request):
    return render(request, 'gym/observaciones.html')

def reglamento(request):
    return render(request, "gym/reglamento.html")



def horario(request):
    return render(request, 'gym/horario.html')

def reportes_exportacion(request):
    return render(request, "gym/reportes_exportacion.html")


def entrenadores(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM obtener_entrenadores()")
        rows = cursor.fetchall()

    entrenadores_list = []
    for r in rows:
        entrenadores_list.append({
            "id_entrenador": r[0],
            "Nombres": r[1],
            "ApellidoM": r[2],
            "ApellidoP": r[3],
            "descrpicion": r[4],
            "url_img": r[5]
        })
    print(entrenadores_list)
    return render(request, "gym/entrenadores.html", {
        "entrenadores": entrenadores_list,
        "MEDIA_URL": settings.MEDIA_URL
    })

def actividades(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sp_select_actividades()")
        columns = [col[0] for col in cursor.description]
        actividades = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, "gym/actividades.html", {"actividades": actividades})
    

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


def administradores(request):   
    return render(request, 'gym/administradores.html')



def crear_admin(request):
    if request.method == "POST":
        usuario = (request.POST.get("usuario") or "").strip()
        password = (request.POST.get("password") or "").strip()

        # Validación básica
        if not usuario or not password:
            messages.error(request, "Por favor complete todos los campos.")
            return render(request, "gym/administradores.html")

        try:
            # Usamos una transacción para mayor seguridad
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO public."Usuarios_admin" ("Usuario", "Password") VALUES (%s, %s);',
                        [usuario, password]
                    )

            messages.success(request, "Administrador creado correctamente.")
        except IntegrityError as e:
            # Manejo específico de llave duplicada (usuario ya existe)
            messages.error(request, "No fue posible crear el administrador: el nombre de usuario ya existe.")
        except Exception as e:
            # Captura errores inesperados y registra/manda mensaje genérico
            # Opcional: loggear 'e' con logging para debug
            messages.error(request, f"No fue posible crear el administrador: {str(e)}")

        # No redirigimos; renderizamos la misma plantilla para que el SweetAlert aparezca
        return render(request, "gym/administradores.html")

    # GET u otros métodos
    return render(request, "gym/administradores.html")

    



def buscar_admin(request):
    """
    Busca administradores:
     - Si no hay parámetros GET renderiza administradores.html.
     - Parámetros aceptados (GET): id_admin (num) y usuario (texto).
     - Devuelve JSON cuando la petición es AJAX; si no, renderiza template con resultados en contexto.
    """
    # Obtener parámetros
    id_param = request.GET.get("id_admin") or request.GET.get("id") or ""
    id_param = id_param.strip()
    nombre = (request.GET.get("usuario") or request.GET.get("nombre") or "").strip()

    # Si no hay criterios -> render
    if not id_param and not nombre: 
                    
        return render(request, "gym/administradores.html")

    try:
        rows = []
        with connection.cursor() as cursor:
            if nombre:
                cursor.execute(
                    """
                    SELECT
                      "id_admin",
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
                # búsqueda por id_admin: consultar directamente la columna id_admin
                try:
                    id_int = int(id_param)
                except (ValueError, TypeError):
                    rows = []
                else:
                    cursor.execute(
                        """
                        SELECT "id_admin", "Usuario"
                        FROM public."Usuarios_admin"
                        WHERE "id_admin" = %s
                        LIMIT 1;
                        """,
                        [id_int]
                    )
                    rows = cursor.fetchall()

        # Mapear resultados a diccionarios
        resultados = [{"id_admin": r[0], "usuario": r[1]} for r in rows]

        # Respuesta AJAX o render normal
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "resultados": resultados})
        else:
            return render(request, "gym/administradores.html", {
                "resultados": resultados,
                "query_usuario": nombre,
                "query_id": id_param
            })

    except Exception as e:
        err = str(e)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": err}, status=500)
        # Renderizar plantilla con mensaje de error en contexto
        return render(request, "gym/administradores.html", {"error": f"No fue posible realizar la búsqueda: {err}"})



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
        numero_empleado = request.POST.get("numero_empleado")    
        if accion == "agregar":
            try:
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT insertar_usuario_general(%s, %s, %s, %s, %s, %s, %s)
                    """, [
                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        tipo_usuario,
                        no_control,
                        numero_empleado,
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
            numero_empleado = request.POST.get("no_control")
   
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT editar_usuario_general(%s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                    id_usuario,
                    nombre,
                    apellido_paterno,
                    apellido_materno,
                    tipo_usuario,
                    no_control if no_control else None,
                    numero_empleado if numero_empleado else None,   # ← NUEVO
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

            # 🔴 Validación desde PostgreSQL
            if mensaje.startswith("Registro inválido"):
                return JsonResponse({
                    "success": False,
                    "error": mensaje
                })

            return JsonResponse({
                "success": True,
                "mensaje": mensaje
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    return JsonResponse({
        "success": False,
        "error": "Método no permitido"
    })

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

def crear_membresia(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método inválido, use POST"
        }, status=400)

    nombre = request.POST.get("nombre_tipo")
    duracion = request.POST.get("duracion")
    costo = request.POST.get("costo_tipo")

    if not nombre or not duracion or not costo:
        return JsonResponse({
            "status": "error",
            "message": "Faltan campos obligatorios"
        }, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT insertar_membresia_general(%s, %s, %s);",
                [nombre, duracion, costo]
            )

        return JsonResponse({
            "status": "success",
            "message": f"Membresía '{nombre}' creada correctamente"
        }, status=200)

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)
        
def obtener_membresias(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM obtener_membresias_general();")
        rows = cursor.fetchall()

    membresias = []
    for row in rows:
        membresias.append({
            "id": row[0],
            "nombre": row[1],
            "duracion": row[2],
            "costo": row[3],
        })

    return JsonResponse({
        "status": "ok",
        "data": membresias
    })
    
@require_POST    
def editar_membresia(request):
    nombre = request.POST.get("nombre")
    duracion = request.POST.get("duracion")
    costo = request.POST.get("costo")

    if not all([nombre, duracion, costo]):
        return JsonResponse({
            "status": "error",
            "message": "Faltan parámetros."
        })

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT editar_membresia_por_nombre(%s, %s, %s);",
            [nombre, duracion, costo]
        )
        result = cursor.fetchone()[0]

    return JsonResponse(result)

@require_POST
def eliminar_membresia(request):
    nombre = request.POST.get("nombre")
    print(request.POST)

    if not nombre:
        return JsonResponse({"status": "error", "message": "Nombre requerido."})

    with connection.cursor() as cursor:
        cursor.execute("SELECT eliminar_membresia_por_nombre(%s);", [nombre])
        result = cursor.fetchone()[0]  # El JSON devuelto por la función

    return JsonResponse(result)





# =========================
# USO DEL GIMNASIO (HISTOGRAMA)
# =========================
def uso_gimnasio_data(request):
    """
    Endpoint JSON para el histograma de uso del gimnasio
    Agrupa entradas por día (lunes a viernes)
    """
    query = """
        SELECT
          EXTRACT(DOW FROM fecha) AS dia,
          COUNT(*) AS total
        FROM ingresos
        WHERE tipo = 'ENTRADA'
          AND EXTRACT(DOW FROM fecha) BETWEEN 1 AND 5
        GROUP BY dia
        ORDER BY dia;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    dias_map = {
        1: "Lunes",
        2: "Martes",
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes"
    }

    labels = []
    data = []

    # Inicializamos todos los días en 0
    conteo_por_dia = {k: 0 for k in dias_map.keys()}

    for dia, total in rows:
        conteo_por_dia[int(dia)] = int(total)

    for dia in range(1, 6):
        labels.append(dias_map[dia])
        data.append(conteo_por_dia[dia])

    return JsonResponse({
        "labels": labels,
        "data": data
    })



from django.http import JsonResponse
from django.db import connection
import json

def uso_gimnasio_por_hora_data(request):
    """
    Endpoint JSON
    Uso del gimnasio por día (L-V) y por hora (8:00–23:00)
    """

    query = """
        SELECT 
          EXTRACT(DOW FROM fecha) AS dia,
          EXTRACT(HOUR FROM fecha) AS hora,
          COUNT(*) AS total
        FROM ingresos
        WHERE tipo = 'ENTRADA'
          AND EXTRACT(DOW FROM fecha) BETWEEN 1 AND 5
          AND EXTRACT(HOUR FROM fecha) BETWEEN 8 AND 23
        GROUP BY dia, hora
        ORDER BY dia, hora;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    dias_map = {
        1: "Lunes",
        2: "Martes",
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes"
    }

    # Inicializar estructura completa (día + hora)
    conteo = {}
    for d in range(1, 6):
        for h in range(8, 24):
            conteo[(d, h)] = 0

    # Llenar con datos reales
    for dia, hora, total in rows:
        conteo[(int(dia), int(hora))] = int(total)

    labels = []
    data = []

    # Generar labels tipo: "Lunes 08:00"
    for d in range(1, 6):
        for h in range(8, 24):
            labels.append(f"{dias_map[d]} {h:02d}:00")
            data.append(conteo[(d, h)])

    return JsonResponse({
        "labels": labels,
        "data": data
    })

def _fetch_users_rows():
    """
    Ejecuta exactamente la consulta SQL que indicaste y devuelve las filas.
    Cada fila: (id_usuario, nombres, apellido_paterno, apellido_materno, tipo)
    """
    query = """
       SELECT u.id_usuario, u.nombres, u.apellido_paterno, u.apellido_materno,
              COALESCE(v.tipo, 'desconocido') AS tipo
       FROM public.usuario u
       LEFT JOIN public.vista_tipo_usuario v ON v.id_usuario = u.id_usuario
       ORDER BY u.id_usuario;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

def _build_counts_from_rows(rows):
    """
    Recibe filas (tuplas) y devuelve:
      - labels: lista de etiquetas (ordenadas)
      - data: lista de conteos (enteros)
      - resumen: lista de dicts para la plantilla [{tipo, conteo}, ...]
      - total: suma de conteos
    Normaliza tipos y mantiene cualquier tipo inesperado al final.
    """
    # contar tipos tal cual vienen (minúsculas tal vez)
    counts = {}
    for r in rows:
        tipo = (r[4] or 'desconocido')
        counts[tipo] = counts.get(tipo, 0) + 1

    # Orden preferido (ajusta si tus tipos en BD usan otras cadenas)
    expected_order = ['alumno', 'representativo', 'externo']
    friendly = {'alumno': 'Alumno', 'representativo': 'Representativo', 'externo': 'Externo', 'desconocido': 'Desconocido'}

    labels = []
    data = []
    # Agregar en orden esperado
    for k in expected_order:
        labels.append(friendly.get(k, k.capitalize()))
        data.append(int(counts.get(k, 0)))

    # Añadir tipos extra que no estén en expected_order (mantener consistencia)
    others = [k for k in counts.keys() if k not in expected_order]
    for k in sorted(others):
        labels.append(friendly.get(k, k.capitalize()))
        data.append(int(counts.get(k, 0)))

    resumen = [{"tipo": labels[i], "conteo": data[i]} for i in range(len(labels))]
    total = sum(data)
    return labels, data, resumen, total

def reportes_view(request):
    """
    Renderiza la plantilla reportes.html con labels_json / data_json derivados
    directamente de la consulta SQL solicitada.
    """
    try:
        rows = _fetch_users_rows()
        labels, data, resumen, total = _build_counts_from_rows(rows)
    except Exception as e:
        return render(request, "gym/graficas.html", {"error": f"Error al consultar la BD: {e}"})

    context = {
        "labels_json": json.dumps(labels),
        "data_json": json.dumps(data),
        "total": total,
        "resumen": resumen,
    }
    return render(request, "gym/graficas.html", context)

def reportes_data(request):
    """
    Endpoint JSON que devuelve los conteos actuales (útil para refrescar las gráficas).
    Respuesta: {"labels": [...], "data": [...], "total": N}
    """
    try:
        rows = _fetch_users_rows()
        labels, data, resumen, total = _build_counts_from_rows(rows)
        return JsonResponse({"labels": labels, "data": data, "total": total})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.db import connection
import io

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import io
from django.http import HttpResponse

# ==========================
# REPORTE USUARIOS
# ==========================
def reporte_usuarios_excel(request):
    wb = Workbook()
    ws_base = wb.active
    wb.remove(ws_base)  # eliminar hoja vacía

    tipos_usuarios = [
        ("Alumnos", "Alumno"),
        ("Representativos", "Representativo"),
        ("Externos", "Externo"),
        ("Desconocidos", "Desconocido"),
        ("Empleados", "Empleado"),
    ]

    for nombre_hoja, tipo in tipos_usuarios:
        query = f"""
            SELECT *
            FROM public.usuario
            WHERE tipo_usuario = '{tipo}'
            ORDER BY id_usuario;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            headers = [col[0] for col in cursor.description]

        ws = wb.create_sheet(title=nombre_hoja)
        ws.append(headers)

        for row in rows:
            ws.append(row)

        # Ajustar ancho de columnas (igual que tus otros excels)
        for i in range(1, len(headers) + 1):
            ws.column_dimensions[get_column_letter(i)].width = 22

    # =========================
    # RESPUESTA HTTP (igual que _exportar_excel)
    # =========================
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="usuarios.xlsx"'
    return response



# ==========================
# REPORTE ENTRADAS Y SALIDAS
# ==========================
def reporte_ingresos_excel(request):
    query = """
      SELECT 
  CASE EXTRACT(DOW FROM fecha)
    WHEN 1 THEN 'Lunes'
    WHEN 2 THEN 'Martes'
    WHEN 3 THEN 'Miércoles'
    WHEN 4 THEN 'Jueves'
    WHEN 5 THEN 'Viernes'
  END AS dia,
  EXTRACT(HOUR FROM fecha) AS hora,
  COUNT(*) AS total
FROM ingresos
WHERE tipo = 'ENTRADA'
  AND EXTRACT(DOW FROM fecha) BETWEEN 1 AND 5
  AND EXTRACT(HOUR FROM fecha) BETWEEN 8 AND 23
GROUP BY dia, hora
ORDER BY 
  MIN(EXTRACT(DOW FROM fecha)), 
  hora;

    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [col[0] for col in cursor.description]

    return _exportar_excel("ingresos.xlsx", headers, rows)


# ==========================
# REPORTE MEMBRESÍAS ACTIVAS
# ==========================
def reporte_membresias_excel(request):
    query = """
        SELECT u.*
        FROM usuario u
        JOIN membresias m ON m.id_usuario = u.id_usuario
        WHERE m.activa = true;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [col[0] for col in cursor.description]

    return _exportar_excel("membresias_activas.xlsx", headers, rows)


# ==========================
# EXCEL
# ==========================
def reporte_observaciones_excel(request):
    query = """
        SELECT *
        FROM observaciones
        ORDER BY fecha_publicacion DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [col[0] for col in cursor.description]

    return _exportar_excel("observaciones.xlsx", headers, rows)


# ==========================
# FUNCIÓN GENÉRICA EXCEL
# ==========================
def _exportar_excel(nombre_archivo, headers, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    ws.append(headers)

    for row in rows:
        ws.append(row)

    for i, col in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = 20

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    return response








def actividad_eliminar(request, id_actividad):
    if request.method != "POST":
        return JsonResponse({'ok': False, 'msg': "Método inválido"}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT sp_delete_actividad(%s);', [id_actividad])

        return JsonResponse({'ok': True, 'message':'Actividad eliminada correctamente', 'success':True})

    except Exception as e:
        return JsonResponse({'ok': False, 'message': str(e)}, status=500)

def actividad_editar(request, id_actividad):
    if request.method != "POST":
        return JsonResponse({'ok': False, 'msg': "Método no permitido"}, status=405)

    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    horario = request.POST.get('horario')

    if not nombre:
        return JsonResponse({'ok': False, 'msg': "El nombre es obligatorio"}, status=422)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sp_update_actividad(%s, %s, %s, %s);",
                [id_actividad, nombre, descripcion, horario]
            )
        return JsonResponse({'ok': True, 'message':'Actividad editada correctamente', 'success':True})

    except Exception as e:
        return JsonResponse({'ok': False, 'message': str(e)}, status=500)
    
def actividad_agregar(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        horario = request.POST.get("horario")

    if not nombre:
        return JsonResponse({'ok': False, 'msg': "Falta nombre"}, status=422)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT sp_insert_actividad(%s, %s, %s);',
                [nombre, descripcion, horario]
            )

        return JsonResponse({
            "success": True,
            "message": "Actividad agregada correctamente."
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Error al agregar la actividad: {e}"
            })
        
def actividades_json(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sp_select_actividades()")
        actividades = cursor.fetchall()

    return JsonResponse({
        "is_admin": bool(request.session.get("usuario_admin")),
        "actividades": [
            {
                "id_actividad": a[0],
                "nombre": a[1],
                "descripcion": a[2],
                "horario": a[3],
            }
            for a in actividades
        ]
    })
    
def editar_entrenador(request, id_entrenador):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)
    try:
        nombres = request.POST.get("nombres")
        apellidoP = request.POST.get("apellidoP")
        apellidoM = request.POST.get("apellidoM")
        descripcion = request.POST.get("descripcion")

        file = request.FILES.get("img")
        nombre_img = None

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT url_imagen
                FROM public."Entrenadores"
                WHERE id_entrenador = %s
            """, [id_entrenador])
            row = cursor.fetchone()
            img_actual = row[0] if row else None

        # ─────────────────────────────────────────
        # 2. Si se sube nueva imagen → guardar y borrar anterior
        # ─────────────────────────────────────────
        if file:
            carpeta = os.path.join(settings.MEDIA_ROOT, "fotosEntrenadores")
            os.makedirs(carpeta, exist_ok=True)

            # Evitar sobrescribir imágenes repetidas
            ext = os.path.splitext(file.name)[1]
            base = os.path.splitext(file.name)[0]
            nombre_img = f"{base}_{int(time.time())}{ext}"

            ruta_nueva = os.path.join(carpeta, nombre_img)

            with open(ruta_nueva, "wb+") as destino:
                for chunk in file.chunks():
                    destino.write(chunk)

            # eliminar imagen anterior
            if img_actual:
                ruta_old = os.path.join(carpeta, img_actual)
                if os.path.exists(ruta_old):
                    os.remove(ruta_old)

        else:
            # No se envió nueva imagen → se conserva la anterior
            nombre_img = img_actual

        # ─────────────────────────────────────────
        # 3. Ejecutar SP
        # ─────────────────────────────────────────
        with connection.cursor() as cursor:
            cursor.callproc(
                "actualizar_entrenador",
                [id_entrenador, nombres, apellidoP, apellidoM, descripcion, nombre_img]
            )
            result = cursor.fetchone()[0]

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Error al actualizar: {str(e)}"
        }, status=500)

def eliminar_entrenador(request, id_entrenador):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

    try:
        # 1️⃣ Obtener el nombre de la imagen antes de eliminar
        with connection.cursor() as cursor:
            cursor.execute('SELECT url_imagen FROM public."Entrenadores" WHERE id_entrenador = %s', [id_entrenador])
            row = cursor.fetchone()

        if not row:
            return JsonResponse({"success": False, "message": "Entrenador no existe"}, status=404)

        imagen = row[0]  # nombre del archivo (ej: "juan.png")

        # 2️⃣ Ejecutar el Stored Procedure de eliminación
        with connection.cursor() as cursor:
            cursor.execute("SELECT eliminar_entrenador(%s);", [id_entrenador])
            result = cursor.fetchone()[0]

        # 3️⃣ Si eliminó correctamente, eliminar el archivo físico
        if result.get("success") and imagen:
            ruta_img = os.path.join(settings.MEDIA_ROOT, "fotosEntrenadores", imagen)
            if os.path.exists(ruta_img):
                os.remove(ruta_img)

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Error al eliminar: {str(e)}"
        }, status=500)
        
def agregar_entrenador(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=400)

    try:
        nombres = request.POST.get("nombres")
        apellidoP = request.POST.get("apellidoP")
        apellidoM = request.POST.get("apellidoM")
        descripcion = request.POST.get("descripcion")
        file = request.FILES.get("img")

        nombre_img = None

        if file:
            carpeta = os.path.join(settings.MEDIA_ROOT, "fotosEntrenadores")
            os.makedirs(carpeta, exist_ok=True)

            # Extensión real del archivo
            extension = os.path.splitext(file.name)[1]
            
            # Generar nombre único
            nombre_img = f"{uuid.uuid4().hex}{extension}"
            ruta = os.path.join(carpeta, nombre_img)

            # Guardar
            with open(ruta, "wb+") as destino:
                for chunk in file.chunks():
                    destino.write(chunk)

        # Guardar datos en BD
        with connection.cursor() as cursor:
            cursor.callproc(
                "insertar_entrenador",
                [nombres, apellidoM, apellidoP, descripcion, nombre_img]
            )

        return JsonResponse({"ok": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def lista_entrenadores_json(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM obtener_entrenadores()')
        rows = cursor.fetchall()

    entrenadores_list = []
    for r in rows:
        entrenadores_list.append({
            "id_entrenador": r[0],
            "Nombres": r[1],
            "ApellidoM": r[2],
            "ApellidoP": r[3],
            "descripcion": r[4],
            "url_img": r[5]
        })

    return JsonResponse({
        "entrenadores": entrenadores_list,
        "MEDIA_URL": settings.MEDIA_URL,
        "usuario_admin": request.session.get("usuario_admin", False)
    })
def buscar_usuario_membresia(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":

        try:
            data = json.loads(request.body)
            id_usuario = data.get("usuario")

            if not id_usuario:
                return JsonResponse({
                    "success": False,
                    "error": "ID de usuario requerido"
                }, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM obtener_membresia_usuario(%s)",
                    [id_usuario]
                )

                columnas = [col[0] for col in cursor.description]
                filas = cursor.fetchall()   # 👈 CAMBIO CLAVE

            # 🔴 No tiene membresía
            if not filas:
                return JsonResponse({
                    "success": True,
                    "tiene_membresia": False
                })

            # 🟢 Tiene membresía (solo 1 por diseño)
            data_sql = dict(zip(columnas, filas[0]))
            print(data_sql)
            return JsonResponse({
                "success": True,
                "tiene_membresia": True,
                "membresia": {
                    "id_membresia": data_sql["id_membresia"],
                    "no_membresia": data_sql["no_membresia"],
                    "nombre_membresia": data_sql["nombre_membresia"],
                    "fecha_inicial": data_sql["fecha_inicial"].strftime("%d/%m/%Y"),
                    "fecha_final": data_sql["fecha_final"].strftime("%d/%m/%Y"),
                    "status": data_sql["status"],
                    "comentario": data_sql["comentario"]
                }
            })

        except Exception as e:
            error = str(e).split("CONTEXT:")[0].strip()
            return JsonResponse({
                "success": False,
                "error": error
            }, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def asignar_membresia_usuario_view(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            data = json.loads(request.body)

            id_usuario = data.get("id_usuario")
            id_membresia = data.get("id_membresia")
            fecha_inicio = data.get("fecha_inicio")
            fecha_fin = data.get("fecha_fin")

            if not all([id_usuario, id_membresia, fecha_inicio, fecha_fin]):
                return JsonResponse({
                    "success": False,
                    "error": "Datos incompletos"
                }, status=400)

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT asignar_membresia_usuario(%s, %s, %s, %s)
                """, [
                    id_usuario,
                    id_membresia,
                    fecha_inicio,
                    fecha_fin
                ])

                mensaje = cursor.fetchone()[0]

            return JsonResponse({
                "success": True,
                "mensaje": mensaje
            })

        except Exception as e:
            error = str(e).split("CONTEXT:")[0].strip()
            return JsonResponse({
                "success": False,
                "error": error
            }, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def actualizar_membresia(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            data = json.loads(request.body)

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT actualizar_membresia_usuario(%s,%s,%s,%s,%s,%s)
                """, [
                    data.get("id_usuario"),
                    data.get("status"),
                    data.get("id_membresia"),      # 👈 puede ser None
                    data.get("fecha_inicial"),     # 👈 puede ser None
                    data.get("fecha_final"),       # 👈 puede ser None
                    data.get("comentario")
                ])

                mensaje = cursor.fetchone()[0]

            return JsonResponse({
                "success": True,
                "mensaje": mensaje
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e).split("CONTEXT:")[0]
            }, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def contador_gimnasio(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT public.contador_gimnasio_hoy();")
        total = cursor.fetchone()[0]

    return JsonResponse({"total": total})   

def agregar_seccion(request):
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descripcion = request.POST.get("descripcion")

        if not tipo or not descripcion:
            return JsonResponse({
                "success": False,
                "mensaje": "Datos incompletos"
            })

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT insertar_regla_header(%s, %s);",
                    [tipo, descripcion]
                )
                mensaje = cursor.fetchone()[0]

            if mensaje != "OK":
                return JsonResponse({
                    "success": False,
                    "mensaje": mensaje
                })
            return JsonResponse({
                "success": True,
                "mensaje": "Seccion agregada correctamente"
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "mensaje": str(e)
            })
        
def reglas_json(request):
    with connection.cursor() as cursor:
        # Headers
        cursor.execute("""
            SELECT tipo, descripcion
            FROM reglas_header
        """)
        headers = cursor.fetchall()

        # Items
        cursor.execute("""
            SELECT tipo, regla
            FROM reglas_item
        """)
        items = cursor.fetchall()

    # Agrupar reglas por tipo
    reglas = []
    for tipo, descripcion in headers:
        reglas.append({
            "tipo": tipo,
            "descripcion": descripcion,
            "items": [r for t, r in items if t == tipo]
        })

    return JsonResponse({"reglas": reglas})


def eliminar_seccion(request):
    if request.method == "POST":
            with connection.cursor() as cursor:
                cursor.execute("SELECT public.contador_gimnasio_hoy();")
                total = cursor.fetchone()[0]

    return JsonResponse({"total": total})     


def guardar_seccion(request):
    if request.method == "POST":
            with connection.cursor() as cursor:
                cursor.execute("SELECT public.contador_gimnasio_hoy();")
                total = cursor.fetchone()[0]

    return JsonResponse({"total": total})     

def reglas_por_seccion(request, tipo):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_regla, regla
                FROM reglas_item
                WHERE tipo = %s
                ORDER BY id_regla
            """, [tipo])

            reglas = [
                {"id": r[0], "regla": r[1]}
                for r in cursor.fetchall()
            ]

        return JsonResponse({
            "success": True,
            "reglas": reglas
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "mensaje": str(e)
        }, status=500)
