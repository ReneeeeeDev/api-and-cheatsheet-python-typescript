"""
CRUD de Estudiantes - Flask + SQLite
Ejecutar:
    pip install flask
    python app.py
Abrir: http://127.0.0.1:5000
API JSON: http://127.0.0.1:5000/api/estudiantes
"""
import csv
import io
import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, Response

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esto"          # necesario para flash()
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "instituto.db")


# ---------------------------------------------------------------- BASE DE DATOS
def get_db():
    """Una conexión por petición, guardada en g."""
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS carreras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL,
        carrera_id INTEGER NOT NULL REFERENCES carreras(id),
        promedio REAL NOT NULL DEFAULT 0
    );
    -- RETO 1: materias y notas (relación N:M entre estudiantes y materias, con la nota)
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        creditos INTEGER NOT NULL CHECK (creditos > 0)
    );
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id) ON DELETE CASCADE,
        materia_id INTEGER NOT NULL REFERENCES materias(id),
        nota REAL NOT NULL CHECK (nota BETWEEN 0 AND 10),
        UNIQUE (estudiante_id, materia_id)
    );
    """)
    if db.execute("SELECT COUNT(*) FROM carreras").fetchone()[0] == 0:
        db.executemany("INSERT INTO carreras (nombre) VALUES (?)",
                       [("Desarrollo de Software",), ("Enfermería",), ("Marketing Digital",)])
        db.executemany(
            "INSERT INTO estudiantes (cedula, nombre, email, carrera_id, promedio) VALUES (?,?,?,?,?)",
            [("1710034065", "Ana Pérez", "ana@mail.com", 1, 9.2),
             ("0926687856", "Luis Mora", "luis@mail.com", 2, 7.5)])
    if db.execute("SELECT COUNT(*) FROM materias").fetchone()[0] == 0:
        db.executemany("INSERT INTO materias (nombre, creditos) VALUES (?, ?)",
                       [("Programación I", 4), ("Base de Datos", 4), ("Inglés", 2)])
        db.executemany("INSERT INTO notas (estudiante_id, materia_id, nota) VALUES (?, ?, ?)",
                       [(1, 1, 9.5), (1, 2, 8.7), (2, 1, 6.0)])
    db.commit()


# ---------------------------------------------------------------- VALIDACIONES
def cedula_valida(cedula: str) -> bool:
    """Algoritmo módulo 10 de la cédula ecuatoriana."""
    if not re.fullmatch(r"\d{10}", cedula):
        return False
    provincia = int(cedula[:2])
    if not (1 <= provincia <= 24 or provincia == 30) or int(cedula[2]) >= 6:
        return False
    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        v = int(cedula[i]) * coef[i]
        total += v - 9 if v > 9 else v
    verificador = (10 - total % 10) % 10
    return verificador == int(cedula[9])


def validar(datos: dict, id_actual=None) -> list:
    errores = []
    nombre = datos.get("nombre", "").strip()
    email = datos.get("email", "").strip()
    cedula = datos.get("cedula", "").strip()
    if len(nombre) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errores.append("Email inválido.")
    if not cedula_valida(cedula):
        errores.append("Cédula ecuatoriana inválida.")
    else:
        fila = get_db().execute("SELECT id FROM estudiantes WHERE cedula = ?", (cedula,)).fetchone()
        if fila and fila["id"] != id_actual:
            errores.append("Ya existe un estudiante con esa cédula.")
    try:
        prom = float(datos.get("promedio", 0))
        if not 0 <= prom <= 10:
            raise ValueError
    except (TypeError, ValueError):
        errores.append("El promedio debe estar entre 0 y 10.")
    try:
        carrera = int(datos.get("carrera_id", 0))
        if not get_db().execute("SELECT 1 FROM carreras WHERE id = ?", (carrera,)).fetchone():
            raise ValueError
    except (TypeError, ValueError):
        errores.append("Seleccione una carrera válida.")
    return errores


# ---------------------------------------------------------------- CONSULTAS
SQL_LISTA = """
SELECT e.*, c.nombre AS carrera
FROM estudiantes e JOIN carreras c ON c.id = e.carrera_id
WHERE e.nombre LIKE ? OR e.cedula LIKE ?
ORDER BY e.nombre
"""
POR_PAGINA = 5


def listar(q="", pagina=None, por_pagina=POR_PAGINA):
    """RETO 2: si se pasa 'pagina' se aplica LIMIT/OFFSET."""
    like = f"%{q}%"
    if pagina is None:
        return get_db().execute(SQL_LISTA, (like, like)).fetchall()
    offset = (pagina - 1) * por_pagina
    return get_db().execute(SQL_LISTA + " LIMIT ? OFFSET ?", (like, like, por_pagina, offset)).fetchall()


def contar(q=""):
    like = f"%{q}%"
    return get_db().execute("SELECT COUNT(*) FROM estudiantes WHERE nombre LIKE ? OR cedula LIKE ?",
                            (like, like)).fetchone()[0]


def obtener(id_):
    return get_db().execute("SELECT * FROM estudiantes WHERE id = ?", (id_,)).fetchone()


def carreras():
    return get_db().execute("SELECT * FROM carreras ORDER BY nombre").fetchall()


def guardar(datos, id_=None):
    valores = (datos["cedula"].strip(), datos["nombre"].strip(), datos["email"].strip(),
               int(datos["carrera_id"]), float(datos.get("promedio", 0)))
    db = get_db()
    if id_ is None:
        cur = db.execute("INSERT INTO estudiantes (cedula, nombre, email, carrera_id, promedio) "
                         "VALUES (?,?,?,?,?)", valores)
        id_ = cur.lastrowid
    else:
        db.execute("UPDATE estudiantes SET cedula=?, nombre=?, email=?, carrera_id=?, promedio=? "
                   "WHERE id=?", valores + (id_,))
    db.commit()
    return id_


# ---------------------------------------------------------------- RUTAS HTML
@app.get("/")
def index():
    q = request.args.get("q", "").strip()
    total = contar(q)
    paginas = max(1, (total + POR_PAGINA - 1) // POR_PAGINA)          # división hacia arriba
    pagina = min(max(1, request.args.get("pagina", 1, type=int)), paginas)
    estudiantes = listar(q, pagina)
    stats = get_db().execute("""
        SELECT c.nombre, COUNT(e.id) AS total, ROUND(AVG(e.promedio), 2) AS promedio
        FROM carreras c LEFT JOIN estudiantes e ON e.carrera_id = c.id
        GROUP BY c.id ORDER BY c.nombre""").fetchall()
    return render_template("index.html", estudiantes=estudiantes, q=q, stats=stats,
                           pagina=pagina, paginas=paginas, total=total)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        errores = validar(request.form)
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("form.html", est=request.form, carreras=carreras(), titulo="Nuevo")
        guardar(request.form)
        flash("Estudiante creado correctamente.", "ok")
        return redirect(url_for("index"))
    return render_template("form.html", est={}, carreras=carreras(), titulo="Nuevo")


@app.route("/editar/<int:id_>", methods=["GET", "POST"])
def editar(id_):
    est = obtener(id_)
    if est is None:
        flash("Estudiante no encontrado.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        errores = validar(request.form, id_actual=id_)
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("form.html", est=request.form, carreras=carreras(), titulo="Editar")
        guardar(request.form, id_)
        flash("Estudiante actualizado.", "ok")
        return redirect(url_for("index"))
    return render_template("form.html", est=est, carreras=carreras(), titulo="Editar")


@app.post("/eliminar/<int:id_>")
def eliminar(id_):
    get_db().execute("DELETE FROM estudiantes WHERE id = ?", (id_,))
    get_db().commit()
    flash("Estudiante eliminado.", "ok")
    return redirect(url_for("index"))


# ---------------------------------------------------------------- RETO 1: NOTAS DEL ESTUDIANTE
@app.route("/estudiantes/<int:id_>/notas", methods=["GET", "POST"])
def notas(id_):
    db = get_db()
    est = db.execute("SELECT e.*, c.nombre AS carrera FROM estudiantes e JOIN carreras c ON c.id = e.carrera_id "
                     "WHERE e.id = ?", (id_,)).fetchone()
    if est is None:
        flash("Estudiante no encontrado.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            materia_id = int(request.form["materia_id"])
            nota = float(request.form["nota"])
            if not 0 <= nota <= 10:
                raise ValueError
        except (KeyError, ValueError):
            flash("Seleccione una materia y una nota entre 0 y 10.", "error")
            return redirect(url_for("notas", id_=id_))
        # UPSERT: si ya tiene nota en esa materia, la actualiza
        db.execute("""INSERT INTO notas (estudiante_id, materia_id, nota) VALUES (?, ?, ?)
                      ON CONFLICT(estudiante_id, materia_id) DO UPDATE SET nota = excluded.nota""",
                   (id_, materia_id, nota))
        actualizar_promedio(id_)
        db.commit()
        flash("Nota registrada.", "ok")
        return redirect(url_for("notas", id_=id_))

    detalle = db.execute("""
        SELECT n.id, m.nombre AS materia, m.creditos, n.nota,
               CASE WHEN n.nota >= 7 THEN 'Aprobado' ELSE 'Reprobado' END AS estado
        FROM notas n JOIN materias m ON m.id = n.materia_id
        WHERE n.estudiante_id = ? ORDER BY m.nombre""", (id_,)).fetchall()
    # Promedio simple y ponderado por créditos, calculados EN SQL
    resumen = db.execute("""
        SELECT COUNT(*) AS materias, ROUND(AVG(n.nota), 2) AS promedio,
               ROUND(SUM(n.nota * m.creditos) * 1.0 / NULLIF(SUM(m.creditos), 0), 2) AS ponderado
        FROM notas n JOIN materias m ON m.id = n.materia_id WHERE n.estudiante_id = ?""", (id_,)).fetchone()
    materias = db.execute("SELECT * FROM materias ORDER BY nombre").fetchall()
    return render_template("notas.html", est=est, detalle=detalle, resumen=resumen, materias=materias)


@app.post("/notas/<int:nota_id>/eliminar")
def eliminar_nota(nota_id):
    db = get_db()
    fila = db.execute("SELECT estudiante_id FROM notas WHERE id = ?", (nota_id,)).fetchone()
    if fila:
        db.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
        actualizar_promedio(fila["estudiante_id"])
        db.commit()
        flash("Nota eliminada.", "ok")
        return redirect(url_for("notas", id_=fila["estudiante_id"]))
    return redirect(url_for("index"))


def actualizar_promedio(estudiante_id):
    """Mantiene sincronizada la columna promedio con las notas registradas."""
    get_db().execute("""UPDATE estudiantes SET promedio = COALESCE(
                            (SELECT ROUND(AVG(nota), 2) FROM notas WHERE estudiante_id = ?), promedio)
                        WHERE id = ?""", (estudiante_id, estudiante_id))


# ---------------------------------------------------------------- RETO 3: EXPORTAR CSV
@app.get("/exportar")
def exportar():
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(["cedula", "nombre", "email", "carrera", "promedio"])
    for e in listar(request.args.get("q", "")):
        escritor.writerow([e["cedula"], e["nombre"], e["email"], e["carrera"], e["promedio"]])
    # \ufeff (BOM) hace que Excel reconozca las tildes
    return Response("\ufeff" + salida.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=estudiantes.csv"})


# ---------------------------------------------------------------- API REST JSON
@app.get("/api/estudiantes")
def api_listar():
    return jsonify([dict(r) for r in listar(request.args.get("q", ""))])


@app.get("/api/estudiantes/<int:id_>")
def api_obtener(id_):
    est = obtener(id_)
    return (jsonify(dict(est)), 200) if est else (jsonify({"error": "No encontrado"}), 404)


@app.post("/api/estudiantes")
def api_crear():
    datos = request.get_json(silent=True) or {}
    datos = {k: str(v) for k, v in datos.items()}
    errores = validar(datos)
    if errores:
        return jsonify({"errores": errores}), 400
    nuevo_id = guardar(datos)
    return jsonify(dict(obtener(nuevo_id))), 201


@app.put("/api/estudiantes/<int:id_>")
def api_actualizar(id_):
    if not obtener(id_):
        return jsonify({"error": "No encontrado"}), 404
    datos = {k: str(v) for k, v in (request.get_json(silent=True) or {}).items()}
    errores = validar(datos, id_actual=id_)
    if errores:
        return jsonify({"errores": errores}), 400
    guardar(datos, id_)
    return jsonify(dict(obtener(id_)))


@app.delete("/api/estudiantes/<int:id_>")
def api_eliminar(id_):
    cur = get_db().execute("DELETE FROM estudiantes WHERE id = ?", (id_,))
    get_db().commit()
    return ("", 204) if cur.rowcount else (jsonify({"error": "No encontrado"}), 404)


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
