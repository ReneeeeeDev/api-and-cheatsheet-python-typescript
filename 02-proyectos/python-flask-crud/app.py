"""
CRUD de Estudiantes - Flask + SQLite
Ejecutar:
    pip install flask
    python app.py
Abrir: http://127.0.0.1:5000
API JSON: http://127.0.0.1:5000/api/estudiantes
"""
import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g

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
    """)
    if db.execute("SELECT COUNT(*) FROM carreras").fetchone()[0] == 0:
        db.executemany("INSERT INTO carreras (nombre) VALUES (?)",
                       [("Desarrollo de Software",), ("Enfermería",), ("Marketing Digital",)])
        db.executemany(
            "INSERT INTO estudiantes (cedula, nombre, email, carrera_id, promedio) VALUES (?,?,?,?,?)",
            [("1710034065", "Ana Pérez", "ana@mail.com", 1, 9.2),
             ("0926687856", "Luis Mora", "luis@mail.com", 2, 7.5)])
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


def listar(q=""):
    like = f"%{q}%"
    return get_db().execute(SQL_LISTA, (like, like)).fetchall()


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
    estudiantes = listar(q)
    stats = get_db().execute("""
        SELECT c.nombre, COUNT(e.id) AS total, ROUND(AVG(e.promedio), 2) AS promedio
        FROM carreras c LEFT JOIN estudiantes e ON e.carrera_id = c.id
        GROUP BY c.id ORDER BY c.nombre""").fetchall()
    return render_template("index.html", estudiantes=estudiantes, q=q, stats=stats)


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
