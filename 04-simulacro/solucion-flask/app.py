"""
SOLUCIÓN DE REFERENCIA del simulacro "Reserva de laboratorios" (Flask + SQLite).
Míralo SOLO después de intentarlo tú.
pip install flask && python app.py   → http://127.0.0.1:5000
Pruebas: python -m unittest -v
"""
import os
import sqlite3
from flask import Flask, g, request, redirect, url_for, flash, render_template_string, jsonify

app = Flask(__name__)
app.config.update(SECRET_KEY="dev", DATABASE=os.path.join(os.path.dirname(__file__), "labs.db"))

ESQUEMA = """
CREATE TABLE IF NOT EXISTS laboratorios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo TEXT NOT NULL UNIQUE,
  nombre TEXT NOT NULL,
  piso INTEGER NOT NULL,
  capacidad INTEGER NOT NULL CHECK (capacidad > 0),
  estado TEXT NOT NULL DEFAULT 'disponible'
);
CREATE TABLE IF NOT EXISTS reservas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  laboratorio_id INTEGER NOT NULL REFERENCES laboratorios(id),
  docente TEXT NOT NULL,
  fecha TEXT NOT NULL,
  hora_inicio TEXT NOT NULL,
  hora_fin TEXT NOT NULL,
  motivo TEXT
);
"""


def db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def cerrar(_):
    if (c := g.pop("db", None)) is not None:
        c.close()


def init_db():
    db().executescript(ESQUEMA)
    if not db().execute("SELECT 1 FROM laboratorios").fetchone():
        db().executemany("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?,?,?,?,?)",
                         [("LAB-001", "Laboratorio de Redes", 1, 25, "disponible"),
                          ("LAB-002", "Laboratorio de Software", 2, 30, "disponible"),
                          ("LAB-003", "Laboratorio Multimedia", 2, 20, "mantenimiento")])
    db().commit()


# ------------------------------------------------------------ REGLAS DE NEGOCIO
def se_cruzan(ini1, fin1, ini2, fin2):
    """Dos intervalos [ini, fin) se cruzan si ini1 < fin2 y ini2 < fin1."""
    return ini1 < fin2 and ini2 < fin1


def validar_laboratorio(f, id_actual=0):
    errores = []
    codigo = f.get("codigo", "").strip().upper()
    if not codigo:
        errores.append("El código es obligatorio.")
    elif db().execute("SELECT 1 FROM laboratorios WHERE codigo = ? AND id <> ?", (codigo, id_actual)).fetchone():
        errores.append("Ya existe un laboratorio con ese código.")
    if len(f.get("nombre", "").strip()) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    for campo, minimo in (("piso", 0), ("capacidad", 1)):
        valor = str(f.get(campo, ""))
        if not valor.isdigit() or int(valor) < minimo:
            errores.append(f"{campo.capitalize()} inválido.")
    if f.get("estado") not in ("disponible", "mantenimiento"):
        errores.append("Estado inválido.")
    return errores


def validar_reserva(f):
    errores = []
    lab = db().execute("SELECT * FROM laboratorios WHERE id = ?", (f.get("laboratorio_id") or 0,)).fetchone()
    ini, fin, fecha = f.get("hora_inicio", ""), f.get("hora_fin", ""), f.get("fecha", "")
    if len(f.get("docente", "").strip()) < 3:
        errores.append("Nombre del docente obligatorio.")
    if not lab:
        errores.append("Seleccione un laboratorio.")
    elif lab["estado"] == "mantenimiento":
        errores.append(f"{lab['nombre']} está en mantenimiento.")
    if not fecha or not ini or not fin:
        errores.append("Fecha y horas son obligatorias.")
    elif fin <= ini:
        errores.append("La hora de fin debe ser mayor a la de inicio.")
    elif lab:
        choque = db().execute("""
            SELECT hora_inicio, hora_fin, docente FROM reservas
            WHERE laboratorio_id = ? AND fecha = ? AND hora_inicio < ? AND ? < hora_fin""",
                              (lab["id"], fecha, fin, ini)).fetchone()
        if choque:
            errores.append(f"Horario ocupado: {choque['hora_inicio']}-{choque['hora_fin']} ({choque['docente']}).")
    return errores


# ------------------------------------------------------------ VISTAS
PLANTILLA = """
<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Reservas de laboratorios</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;background:#f1f5f9;color:#1f2937}
header{background:#0a5bd6;color:#fff;padding:12px 20px;display:flex;gap:16px;align-items:center}
header a{color:#fff}main{max-width:1000px;margin:20px auto;padding:0 16px;display:grid;gap:16px}
.panel{background:#fff;padding:16px;border-radius:10px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
label{display:grid;gap:4px;font-size:14px}input,select{padding:8px;border:1px solid #cbd5e1;border-radius:6px;width:100%}
button{padding:8px 14px;border:0;border-radius:6px;background:#0a5bd6;color:#fff;cursor:pointer}
.peligro{background:#dc2626}table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #e5e7eb;text-align:left}
.ok{background:#dcfce7;color:#166534;padding:10px;border-radius:6px}.error{background:#fee2e2;color:#991b1b;padding:10px;border-radius:6px}
.mant{color:#dc2626;font-weight:600}form.inline{display:inline}
</style></head><body>
<header><strong>Reservas ISTE</strong><a href="{{ url_for('laboratorios') }}">Laboratorios</a>
<a href="{{ url_for('reservas') }}">Reservas</a><a href="{{ url_for('reporte') }}">Reporte</a></header>
<main>
{% for cat, m in get_flashed_messages(with_categories=true) %}<div class="{{ cat }}">{{ m }}</div>{% endfor %}
{{ contenido|safe }}
</main></body></html>
"""


def render(contenido_tpl, **ctx):
    contenido = render_template_string(contenido_tpl, **ctx)
    return render_template_string(PLANTILLA, contenido=contenido)


LABS_TPL = """
<section class="panel"><h2>{{ 'Editar ' ~ lab.codigo if lab.id else 'Nuevo laboratorio' }}</h2>
<form method="post" action="{{ url_for('guardar_laboratorio', id_=lab.id or 0) }}"><div class="grid">
<label>Código<input name="codigo" value="{{ lab.codigo or '' }}" required></label>
<label>Nombre<input name="nombre" value="{{ lab.nombre or '' }}" required></label>
<label>Piso<input name="piso" type="number" min="0" value="{{ lab.piso if lab.piso is not none else '' }}" required></label>
<label>Capacidad<input name="capacidad" type="number" min="1" value="{{ lab.capacidad or '' }}" required></label>
<label>Estado<select name="estado">{% for e in ['disponible','mantenimiento'] %}
<option {{ 'selected' if lab.estado == e }}>{{ e }}</option>{% endfor %}</select></label>
</div><p><button>Guardar</button> {% if lab.id %}<a href="{{ url_for('laboratorios') }}">Cancelar</a>{% endif %}</p></form></section>
<section class="panel"><table><tr><th>Código</th><th>Nombre</th><th>Piso</th><th>Capacidad</th><th>Estado</th><th></th></tr>
{% for l in labs %}<tr><td>{{ l.codigo }}</td><td>{{ l.nombre }}</td><td>{{ l.piso }}</td><td>{{ l.capacidad }}</td>
<td class="{{ 'mant' if l.estado == 'mantenimiento' }}">{{ l.estado }}</td>
<td><a href="{{ url_for('laboratorios', editar=l.id) }}">Editar</a>
<form class="inline" method="post" action="{{ url_for('eliminar_laboratorio', id_=l.id) }}" onsubmit="return confirm('¿Eliminar?')">
<button class="peligro">Eliminar</button></form></td></tr>{% endfor %}</table></section>
"""


@app.get("/")
@app.get("/laboratorios")
def laboratorios(form=None):
    labs = db().execute("SELECT * FROM laboratorios ORDER BY codigo").fetchall()
    lab = form or {}
    if not form and request.args.get("editar"):
        fila = db().execute("SELECT * FROM laboratorios WHERE id = ?", (request.args["editar"],)).fetchone()
        lab = dict(fila) if fila else {}
    return render(LABS_TPL, labs=labs, lab=lab)


@app.post("/laboratorios/<int:id_>")
def guardar_laboratorio(id_):
    f = request.form
    errores = validar_laboratorio(f, id_)
    if errores:
        for e in errores:
            flash(e, "error")
        return laboratorios(form={**f, "id": id_}), 400
    datos = (f["codigo"].strip().upper(), f["nombre"].strip(), int(f["piso"]), int(f["capacidad"]), f["estado"])
    if id_:
        db().execute("UPDATE laboratorios SET codigo=?, nombre=?, piso=?, capacidad=?, estado=? WHERE id=?", datos + (id_,))
    else:
        db().execute("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?,?,?,?,?)", datos)
    db().commit()
    flash("Laboratorio guardado.", "ok")
    return redirect(url_for("laboratorios"))


@app.post("/laboratorios/<int:id_>/eliminar")
def eliminar_laboratorio(id_):
    if db().execute("SELECT 1 FROM reservas WHERE laboratorio_id = ?", (id_,)).fetchone():
        flash("No se puede eliminar: el laboratorio tiene reservas.", "error")
    else:
        db().execute("DELETE FROM laboratorios WHERE id = ?", (id_,))
        db().commit()
        flash("Laboratorio eliminado.", "ok")
    return redirect(url_for("laboratorios"))


RESERVAS_TPL = """
<section class="panel"><h2>Nueva reserva</h2><form method="post"><div class="grid">
<label>Docente<input name="docente" value="{{ f.docente or '' }}" required></label>
<label>Laboratorio<select name="laboratorio_id" required><option value="">--</option>
{% for l in labs %}<option value="{{ l.id }}" {{ 'selected' if (f.laboratorio_id|string) == (l.id|string) }}>
{{ l.codigo }} - {{ l.nombre }}{{ ' (mantenimiento)' if l.estado == 'mantenimiento' }}</option>{% endfor %}</select></label>
<label>Fecha<input type="date" name="fecha" value="{{ f.fecha or '' }}" required></label>
<label>Inicio<input type="time" name="hora_inicio" value="{{ f.hora_inicio or '' }}" required></label>
<label>Fin<input type="time" name="hora_fin" value="{{ f.hora_fin or '' }}" required></label>
<label>Motivo<input name="motivo" value="{{ f.motivo or '' }}"></label>
</div><p><button>Reservar</button></p></form></section>
<section class="panel"><form method="get" class="grid">
<label>Filtrar fecha<input type="date" name="fecha" value="{{ filtro_fecha }}"></label>
<label>Filtrar laboratorio<select name="lab"><option value="">Todos</option>
{% for l in labs %}<option value="{{ l.id }}" {{ 'selected' if filtro_lab == l.id|string }}>{{ l.codigo }}</option>{% endfor %}</select></label>
<label>&nbsp;<button>Filtrar</button></label></form>
<table><tr><th>Fecha</th><th>Horario</th><th>Laboratorio</th><th>Docente</th><th>Motivo</th><th></th></tr>
{% for r in reservas %}<tr><td>{{ r.fecha }}</td><td>{{ r.hora_inicio }}-{{ r.hora_fin }}</td><td>{{ r.laboratorio }}</td>
<td>{{ r.docente }}</td><td>{{ r.motivo or '' }}</td><td><form class="inline" method="post" action="{{ url_for('eliminar_reserva', id_=r.id) }}">
<button class="peligro">Cancelar</button></form></td></tr>{% else %}<tr><td colspan="6">Sin reservas</td></tr>{% endfor %}
</table></section>
"""


@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    f, status = {}, 200
    if request.method == "POST":
        f = request.form
        errores = validar_reserva(f)
        if errores:
            for e in errores:
                flash(e, "error")
            status = 400
        else:
            db().execute("INSERT INTO reservas (laboratorio_id, docente, fecha, hora_inicio, hora_fin, motivo) "
                         "VALUES (?,?,?,?,?,?)", (f["laboratorio_id"], f["docente"].strip(), f["fecha"],
                                                  f["hora_inicio"], f["hora_fin"], f.get("motivo", "").strip()))
            db().commit()
            flash("Reserva registrada.", "ok")
            return redirect(url_for("reservas"))
    filtro_fecha, filtro_lab = request.args.get("fecha", ""), request.args.get("lab", "")
    sql = ("SELECT r.*, l.codigo || ' - ' || l.nombre AS laboratorio FROM reservas r "
           "JOIN laboratorios l ON l.id = r.laboratorio_id WHERE 1=1")
    params = []
    if filtro_fecha:
        sql += " AND r.fecha = ?"
        params.append(filtro_fecha)
    if filtro_lab:
        sql += " AND r.laboratorio_id = ?"
        params.append(filtro_lab)
    filas = db().execute(sql + " ORDER BY r.fecha, r.hora_inicio", params).fetchall()
    labs = db().execute("SELECT * FROM laboratorios ORDER BY codigo").fetchall()
    return render(RESERVAS_TPL, labs=labs, reservas=filas, f=f,
                  filtro_fecha=filtro_fecha, filtro_lab=filtro_lab), status


@app.post("/reservas/<int:id_>/eliminar")
def eliminar_reserva(id_):
    db().execute("DELETE FROM reservas WHERE id = ?", (id_,))
    db().commit()
    flash("Reserva cancelada.", "ok")
    return redirect(url_for("reservas"))


SQL_REPORTE = """
SELECT l.codigo, l.nombre, COUNT(r.id) AS reservas,
  ROUND(COALESCE(SUM((strftime('%s', r.hora_fin) - strftime('%s', r.hora_inicio)) / 3600.0), 0), 1) AS horas
FROM laboratorios l LEFT JOIN reservas r ON r.laboratorio_id = l.id
GROUP BY l.id ORDER BY horas DESC
"""


@app.get("/reporte")
def reporte():
    filas = db().execute(SQL_REPORTE).fetchall()
    return render("""<section class="panel"><h2>Uso de laboratorios</h2><table>
    <tr><th>Código</th><th>Laboratorio</th><th>Reservas</th><th>Horas</th></tr>
    {% for f in filas %}<tr><td>{{ f.codigo }}</td><td>{{ f.nombre }}</td><td>{{ f.reservas }}</td><td>{{ f.horas }}</td></tr>{% endfor %}
    </table></section>""", filas=filas)


# ------------------------------------------------------------ API
@app.get("/api/laboratorios")
def api_labs():
    return jsonify([dict(r) for r in db().execute("SELECT * FROM laboratorios ORDER BY codigo")])


@app.post("/api/laboratorios")
def api_crear_lab():
    f = {k: str(v) for k, v in (request.get_json(silent=True) or {}).items()}
    f.setdefault("estado", "disponible")
    errores = validar_laboratorio(f)
    if errores:
        return jsonify({"errores": errores}), 400
    cur = db().execute("INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?,?,?,?,?)",
                       (f["codigo"].strip().upper(), f["nombre"].strip(), int(f["piso"]), int(f["capacidad"]), f["estado"]))
    db().commit()
    return jsonify(dict(db().execute("SELECT * FROM laboratorios WHERE id = ?", (cur.lastrowid,)).fetchone())), 201


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
