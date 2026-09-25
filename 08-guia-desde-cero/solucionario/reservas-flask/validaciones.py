"""Reglas de negocio. Cada función recibe la conexión (db) y los datos del formulario
y devuelve una lista de mensajes de error (lista vacía = todo correcto)."""
import re

ESTADOS = ("disponible", "mantenimiento")
PATRON_HORA = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")      # 00:00 a 23:59
PATRON_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")           # 2026-09-25


def se_cruzan(ini1, fin1, ini2, fin2):
    """Dos horarios [ini, fin) se cruzan si uno empieza antes de que termine el otro.
    Las horas en formato HH:MM se pueden comparar como texto."""
    return ini1 < fin2 and ini2 < fin1


def es_entero(valor, minimo):
    texto = str(valor).strip()
    return texto.isdigit() and int(texto) >= minimo


def validar_laboratorio(db, datos, id_actual=0):
    errores = []
    codigo = str(datos.get("codigo", "")).strip().upper()
    nombre = str(datos.get("nombre", "")).strip()

    if not codigo:
        errores.append("El código es obligatorio.")
    elif db.execute("SELECT 1 FROM laboratorios WHERE codigo = ? AND id <> ?",
                    (codigo, id_actual)).fetchone():
        errores.append(f"Ya existe un laboratorio con el código {codigo}.")

    if len(nombre) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    if not es_entero(datos.get("piso", ""), 0):
        errores.append("El piso debe ser un número entero (0 o mayor).")
    if not es_entero(datos.get("capacidad", ""), 1):
        errores.append("La capacidad debe ser un número entero mayor a 0.")
    if datos.get("estado", "disponible") not in ESTADOS:
        errores.append("El estado debe ser 'disponible' o 'mantenimiento'.")
    return errores


def buscar_choque(db, laboratorio_id, fecha, hora_inicio, hora_fin):
    """Devuelve la reserva que se cruza con el horario pedido, o None."""
    return db.execute(
        """SELECT * FROM reservas
           WHERE laboratorio_id = ? AND fecha = ?
             AND hora_inicio < ? AND ? < hora_fin""",
        (laboratorio_id, fecha, hora_fin, hora_inicio),
    ).fetchone()


def validar_reserva(db, datos):
    errores = []
    docente = str(datos.get("docente", "")).strip()
    fecha = str(datos.get("fecha", ""))
    inicio = str(datos.get("hora_inicio", ""))
    fin = str(datos.get("hora_fin", ""))
    lab = db.execute("SELECT * FROM laboratorios WHERE id = ?",
                     (datos.get("laboratorio_id") or 0,)).fetchone()

    if len(docente) < 3:
        errores.append("El nombre del docente es obligatorio (mínimo 3 caracteres).")
    if lab is None:
        errores.append("Seleccione un laboratorio válido.")
    elif lab["estado"] == "mantenimiento":
        errores.append(f"{lab['nombre']} está en mantenimiento y no se puede reservar.")
    if not PATRON_FECHA.match(fecha):
        errores.append("La fecha es obligatoria.")
    if not (PATRON_HORA.match(inicio) and PATRON_HORA.match(fin)):
        errores.append("Las horas de inicio y fin son obligatorias (HH:MM).")
    elif fin <= inicio:
        errores.append("La hora de fin debe ser mayor que la hora de inicio.")

    # Solo buscamos choques si lo anterior está bien
    if not errores:
        choque = buscar_choque(db, lab["id"], fecha, inicio, fin)
        if choque:
            errores.append(f"Horario ocupado: {choque['hora_inicio']}-{choque['hora_fin']} "
                           f"reservado por {choque['docente']}.")
    return errores
