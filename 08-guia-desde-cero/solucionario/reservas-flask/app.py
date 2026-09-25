"""Sistema de reserva de laboratorios - Flask + SQLite."""
import os

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from db import close_db, get_db, init_db
from validaciones import validar_laboratorio, validar_reserva

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esta-clave"          # necesario para flash()
app.config["DATABASE"] = os.path.join(app.root_path, "reservas.db")
app.teardown_appcontext(close_db)                         # cierra la BD al final de cada petición


@app.get("/")
def inicio():
    db = get_db()
    totales = {
        "laboratorios": db.execute("SELECT COUNT(*) FROM laboratorios").fetchone()[0],
        "disponibles": db.execute(
            "SELECT COUNT(*) FROM laboratorios WHERE estado = 'disponible'").fetchone()[0],
        "reservas": db.execute("SELECT COUNT(*) FROM reservas").fetchone()[0],
    }
    return render_template("inicio.html", totales=totales)


# ----------------------------------------------------------- LABORATORIOS (CRUD)
def datos_laboratorio(f):
    """Limpia y convierte los datos del formulario al orden de las columnas."""
    return (f["codigo"].strip().upper(), f["nombre"].strip(), int(f["piso"]),
            int(f["capacidad"]), f.get("estado", "disponible"))


def mostrar_laboratorios(form=None, errores=None, status=200):
    labs = get_db().execute("SELECT * FROM laboratorios ORDER BY codigo").fetchall()
    return render_template("laboratorios.html", labs=labs, form=form or {},
                           errores=errores or []), status


@app.get("/laboratorios")
def laboratorios():
    editar_id = request.args.get("editar", type=int)
    if editar_id:                                   # /laboratorios?editar=2 → carga el formulario
        lab = get_db().execute("SELECT * FROM laboratorios WHERE id = ?", (editar_id,)).fetchone()
        if lab is None:
            flash("Laboratorio no encontrado.", "error")
            return redirect(url_for("laboratorios"))
        return mostrar_laboratorios(form=dict(lab))
    return mostrar_laboratorios()


@app.post("/laboratorios")
def crear_laboratorio():
    db = get_db()
    errores = validar_laboratorio(db, request.form)
    if errores:
        return mostrar_laboratorios(request.form, errores, 400)
    db.execute("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) "
               "VALUES (?, ?, ?, ?, ?)", datos_laboratorio(request.form))
    db.commit()
    flash("Laboratorio creado correctamente.", "ok")
    return redirect(url_for("laboratorios"))          # patrón POST → redirect → GET


@app.post("/laboratorios/<int:lab_id>")
def actualizar_laboratorio(lab_id):
    db = get_db()
    errores = validar_laboratorio(db, request.form, id_actual=lab_id)
    if errores:
        return mostrar_laboratorios({**request.form, "id": lab_id}, errores, 400)
    db.execute("UPDATE laboratorios SET codigo = ?, nombre = ?, piso = ?, capacidad = ?, "
               "estado = ? WHERE id = ?", datos_laboratorio(request.form) + (lab_id,))
    db.commit()
    flash("Laboratorio actualizado.", "ok")
    return redirect(url_for("laboratorios"))


@app.post("/laboratorios/<int:lab_id>/eliminar")
def eliminar_laboratorio(lab_id):
    db = get_db()
    if db.execute("SELECT 1 FROM reservas WHERE laboratorio_id = ?", (lab_id,)).fetchone():
        flash("No se puede eliminar: el laboratorio tiene reservas registradas.", "error")
    else:
        db.execute("DELETE FROM laboratorios WHERE id = ?", (lab_id,))
        db.commit()
        flash("Laboratorio eliminado.", "ok")
    return redirect(url_for("laboratorios"))


# ----------------------------------------------------------- RESERVAS
def mostrar_reservas(form=None, errores=None, status=200):
    db = get_db()
    filtro = {"fecha": request.args.get("fecha", ""), "lab": request.args.get("lab", "")}

    sql = """SELECT r.*, l.codigo, l.nombre AS laboratorio
             FROM reservas r
             JOIN laboratorios l ON l.id = r.laboratorio_id
             WHERE 1 = 1"""
    params = []
    if filtro["fecha"]:
        sql += " AND r.fecha = ?"
        params.append(filtro["fecha"])
    if filtro["lab"]:
        sql += " AND r.laboratorio_id = ?"
        params.append(filtro["lab"])
    sql += " ORDER BY r.fecha, r.hora_inicio"

    return render_template(
        "reservas.html",
        reservas=db.execute(sql, params).fetchall(),
        labs=db.execute("SELECT * FROM laboratorios ORDER BY codigo").fetchall(),
        form=form or {}, errores=errores or [], filtro=filtro,
    ), status


@app.get("/reservas")
def reservas():
    return mostrar_reservas()


@app.post("/reservas")
def crear_reserva():
    db = get_db()
    f = request.form
    errores = validar_reserva(db, f)
    if errores:
        return mostrar_reservas(f, errores, 400)
    db.execute("INSERT INTO reservas (laboratorio_id, docente, fecha, hora_inicio, hora_fin, motivo) "
               "VALUES (?, ?, ?, ?, ?, ?)",
               (int(f["laboratorio_id"]), f["docente"].strip(), f["fecha"],
                f["hora_inicio"], f["hora_fin"], f.get("motivo", "").strip()))
    db.commit()
    flash("Reserva registrada.", "ok")
    return redirect(url_for("reservas"))


@app.post("/reservas/<int:reserva_id>/eliminar")
def eliminar_reserva(reserva_id):
    db = get_db()
    db.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    db.commit()
    flash("Reserva cancelada.", "ok")
    return redirect(url_for("reservas"))


# ----------------------------------------------------------- REPORTE
SQL_REPORTE = """
SELECT l.codigo, l.nombre,
       COUNT(r.id) AS total_reservas,
       ROUND(COALESCE(SUM(
           (strftime('%s', r.hora_fin) - strftime('%s', r.hora_inicio)) / 3600.0
       ), 0), 1) AS horas
FROM laboratorios l
LEFT JOIN reservas r ON r.laboratorio_id = l.id
GROUP BY l.id
ORDER BY horas DESC, l.codigo
"""


@app.get("/reporte")
def reporte():
    filas = get_db().execute(SQL_REPORTE).fetchall()
    return render_template("reporte.html", filas=filas)


# ----------------------------------------------------------- API REST (JSON)
@app.get("/api/laboratorios")
def api_listar_laboratorios():
    filas = get_db().execute("SELECT * FROM laboratorios ORDER BY codigo").fetchall()
    return jsonify([dict(f) for f in filas])


@app.post("/api/laboratorios")
def api_crear_laboratorio():
    datos = request.get_json(silent=True) or {}
    datos = {k: str(v) for k, v in datos.items()}      # todo a texto, igual que un formulario
    datos.setdefault("estado", "disponible")
    db = get_db()
    errores = validar_laboratorio(db, datos)
    if errores:
        return jsonify({"errores": errores}), 400
    cur = db.execute("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) "
                     "VALUES (?, ?, ?, ?, ?)", datos_laboratorio(datos))
    db.commit()
    nuevo = db.execute("SELECT * FROM laboratorios WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(nuevo)), 201


@app.get("/api/reservas")
def api_listar_reservas():
    fecha = request.args.get("fecha")
    sql = ("SELECT r.*, l.codigo FROM reservas r JOIN laboratorios l ON l.id = r.laboratorio_id")
    params = []
    if fecha:
        sql += " WHERE r.fecha = ?"
        params.append(fecha)
    return jsonify([dict(f) for f in get_db().execute(sql + " ORDER BY r.fecha, r.hora_inicio", params)])


# ----------------------------------------------------------- ARRANQUE
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
