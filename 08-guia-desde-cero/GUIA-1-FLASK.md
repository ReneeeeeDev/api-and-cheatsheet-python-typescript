# Guía 1 — Construir desde cero con Python + Flask

**App:** Sistema de reserva de laboratorios (el simulacro).
**Resultado:** CRUD de laboratorios, reservas sin cruces de horario, filtros, reporte, API JSON y pruebas.
**Tiempo objetivo:** 2 h 15 min. Cada paso termina con **✅ Verifica** y **💾 Commit**.

> La carpeta `solucionario/reservas-flask` tiene el proyecto terminado. Todo el código de esta guía sale de ahí, así que si algo no te funciona, compara tu archivo con el del solucionario.

## Mapa de pasos

| Paso | Qué haces | Min | Acumulado |
|---|---|---|---|
| 0 | Verificar herramientas | 3 | 0:03 |
| 1 | Leer y diseñar (tablas y rutas) | 10 | 0:13 |
| 2 | Crear el proyecto y las carpetas | 10 | 0:23 |
| 3 | Base de datos | 10 | 0:33 |
| 4 | Reglas de negocio (validaciones) | 15 | 0:48 |
| 5 | App base + plantilla HTML + CSS | 15 | 1:03 |
| 6 | CRUD de laboratorios | 25 | 1:28 |
| 7 | Reservas + filtros | 25 | 1:53 |
| 8 | Reporte | 7 | 2:00 |
| 9 | API JSON | 7 | 2:07 |
| 10 | Pruebas automáticas | 8 | 2:15 |
| 11 | README + GitHub | 10 | 2:25 |

Si vas atrasado, **salta el 10** (pruebas) y haz el 11. El orden prioriza que siempre tengas algo funcionando.

---

## Paso 0 — Verificar herramientas (3 min)

Abre una terminal (en Windows: **PowerShell** o la terminal de VS Code con `Ctrl + ñ`).

```bash
python --version        # debe decir 3.8 o mayor. Si no funciona, prueba: py --version
pip --version           # si no funciona: python -m pip --version
git --version
code --version          # VS Code (opcional)
```

Si `python` no existe pero `py` sí, usa `py` en todos los comandos de esta guía.

---

## Paso 1 — Leer y diseñar antes de programar (10 min)

En una hoja escribe esto. Dedicarle 10 minutos te ahorra 30 después.

**Tablas:**
```
laboratorios                         reservas
------------                         --------
id (PK)                              id (PK)
codigo (único)       1 ───────── N   laboratorio_id (FK → laboratorios.id)
nombre                               docente
piso                                 fecha        (AAAA-MM-DD)
capacidad (> 0)                      hora_inicio  (HH:MM)
estado (disponible|mantenimiento)    hora_fin     (HH:MM)
                                     motivo
```

**Rutas (URLs):**

| Método | URL | Qué hace |
|---|---|---|
| GET | `/` | Panel con totales |
| GET | `/laboratorios` | Listado + formulario (con `?editar=ID` carga uno para editar) |
| POST | `/laboratorios` | Crear |
| POST | `/laboratorios/<id>` | Actualizar |
| POST | `/laboratorios/<id>/eliminar` | Eliminar |
| GET | `/reservas` | Listado con filtros `?fecha=&lab=` + formulario |
| POST | `/reservas` | Crear reserva |
| POST | `/reservas/<id>/eliminar` | Cancelar reserva |
| GET | `/reporte` | Reservas y horas por laboratorio |
| GET/POST | `/api/laboratorios` | API JSON |
| GET | `/api/reservas` | API JSON |

> Los formularios HTML solo envían GET y POST. Por eso editar y eliminar usan POST con URLs distintas. En una API JSON usarías PUT y DELETE.

**Regla clave (choque de horarios):** dos reservas del mismo laboratorio y el mismo día chocan si `inicio_nueva < fin_existente` **y** `inicio_existente < fin_nueva`.

---

## Paso 2 — Crear el proyecto y las carpetas (10 min)

### 2.1 Crear la carpeta y el entorno virtual

```bash
# Ubícate donde quieras el proyecto (Escritorio, Documentos...)
cd Desktop
mkdir reservas-flask
cd reservas-flask

# Entorno virtual: aísla las librerías de este proyecto
python -m venv venv
```

Activa el entorno (hazlo **cada vez** que abras una terminal nueva):

```bash
venv\Scripts\activate           # Windows (PowerShell o CMD)
source venv/bin/activate        # Linux / Mac
```

Cuando está activo, la línea de la terminal empieza con `(venv)`.

> **Si PowerShell dice "la ejecución de scripts está deshabilitada":**
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a activar.

### 2.2 Instalar Flask y registrar dependencias

```bash
pip install flask
pip freeze > requirements.txt
```

`requirements.txt` sirve para que otra persona instale lo mismo con `pip install -r requirements.txt`.

### 2.3 Crear la estructura de carpetas

```bash
mkdir templates
mkdir static
mkdir static\css          # Linux/Mac: mkdir -p static/css
mkdir tests
```

Estructura final a la que vamos a llegar:

```
reservas-flask/
├── venv/                  ← entorno virtual (NO se sube a Git)
├── app.py                 ← rutas: recibe peticiones y responde (controlador)
├── db.py                  ← conexión a la base de datos
├── schema.sql             ← creación de tablas
├── validaciones.py        ← reglas de negocio (qué datos son válidos)
├── requirements.txt       ← dependencias
├── README.md              ← cómo instalar y ejecutar
├── .gitignore             ← qué NO subir a Git
├── templates/             ← HTML con Jinja2 (Flask busca aquí por defecto)
│   ├── base.html          ← esqueleto común (menú, mensajes)
│   ├── inicio.html
│   ├── laboratorios.html
│   ├── reservas.html
│   └── reporte.html
├── static/                ← archivos públicos (Flask los sirve en /static/...)
│   └── css/styles.css
└── tests/
    └── test_app.py
```

**¿Por qué separar así?** Cada archivo tiene una sola responsabilidad: `db.py` sabe hablar con la BD, `validaciones.py` sabe qué es válido y `app.py` une todo. Es una versión simple de **MVC**: el modelo son `db.py` + `schema.sql` + `validaciones.py`, la vista son los `templates/` y el controlador es `app.py`. Si el evaluador te pregunta, eso es lo que responde.

> Los nombres `templates` y `static` **no se pueden cambiar**: Flask los busca con esos nombres.

### 2.4 Git

Crea el archivo `.gitignore` en la raíz del proyecto:

```text
venv/
__pycache__/
*.db
.vscode/
```

```bash
git init
git config user.name "Tu Nombre"          # si la PC del laboratorio no lo tiene
git config user.email "tu@correo.com"
git add .
git commit -m "chore: estructura inicial del proyecto Flask"
```

Abre la carpeta en VS Code: `code .`

✅ **Verifica:** `git status` dice "nothing to commit" y `venv/` no aparece en `git status`.

---

## Paso 3 — Base de datos (10 min)

Usamos **SQLite**, que viene incluido con Python: no hay que instalar nada y la BD es un archivo (`reservas.db`).

### 3.1 `schema.sql` — las tablas

```sql
-- Esquema de la base de datos (SQLite).
-- "IF NOT EXISTS" permite ejecutarlo cada vez que arranca la app sin borrar datos.

CREATE TABLE IF NOT EXISTS laboratorios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT    NOT NULL UNIQUE,
    nombre      TEXT    NOT NULL,
    piso        INTEGER NOT NULL CHECK (piso >= 0),
    capacidad   INTEGER NOT NULL CHECK (capacidad > 0),
    estado      TEXT    NOT NULL DEFAULT 'disponible'
                CHECK (estado IN ('disponible', 'mantenimiento'))
);

CREATE TABLE IF NOT EXISTS reservas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    laboratorio_id  INTEGER NOT NULL REFERENCES laboratorios(id),
    docente         TEXT    NOT NULL,
    fecha           TEXT    NOT NULL,          -- formato AAAA-MM-DD
    hora_inicio     TEXT    NOT NULL,          -- formato HH:MM
    hora_fin        TEXT    NOT NULL,
    motivo          TEXT,
    CHECK (hora_fin > hora_inicio)
);
```

Puntos a notar:
- `UNIQUE` en `codigo`: la BD misma impide duplicados.
- `REFERENCES laboratorios(id)`: clave foránea (FK).
- Los `CHECK` son una segunda línea de defensa. La validación principal la hacemos en Python para mostrar mensajes claros.

### 3.2 `db.py` — conexión

```python
"""Conexión a la base de datos SQLite (una conexión por petición)."""
import sqlite3

from flask import current_app, g


def get_db():
    """Devuelve la conexión de esta petición; la crea si no existe."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row          # permite fila["columna"]
        g.db.execute("PRAGMA foreign_keys = ON")  # SQLite no activa las FK por defecto
    return g.db


def close_db(error=None):
    """Flask la llama automáticamente al terminar cada petición."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Crea las tablas y carga datos de ejemplo si la tabla está vacía."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))

    vacia = db.execute("SELECT COUNT(*) FROM laboratorios").fetchone()[0] == 0
    if vacia:
        db.executemany(
            "INSERT INTO laboratorios (codigo, nombre, piso, capacidad, estado) VALUES (?, ?, ?, ?, ?)",
            [
                ("LAB-001", "Laboratorio de Redes", 1, 25, "disponible"),
                ("LAB-002", "Laboratorio de Software", 2, 30, "disponible"),
                ("LAB-003", "Laboratorio Multimedia", 2, 20, "mantenimiento"),
            ],
        )
    db.commit()
```

**Qué hace cada parte:**
- `g` es un objeto de Flask que vive solo durante una petición. Guardamos ahí la conexión para reutilizarla.
- `row_factory = sqlite3.Row` permite escribir `fila["nombre"]` en lugar de `fila[2]`.
- `current_app.open_resource("schema.sql")` abre el archivo relativo a la carpeta del proyecto.
- `executemany` inserta varias filas con **parámetros `?`**. **Nunca** armes SQL concatenando texto del usuario: eso es SQL Injection.

💾 `git add . ; git commit -m "feat: esquema de base de datos y conexión"`

> El `;` separa dos comandos y funciona tanto en PowerShell como en Git Bash. En CMD escribe los dos comandos por separado.

---

## Paso 4 — Reglas de negocio (15 min)

### `validaciones.py`

```python
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
```

**Por qué funciona la consulta de choque:** buscamos reservas del mismo laboratorio y la misma fecha donde `hora_inicio_existente < hora_fin_nueva` **y** `hora_inicio_nueva < hora_fin_existente`. Ejemplos:

| Existente | Nueva | ¿Choca? | Por qué |
|---|---|---|---|
| 08:00–10:00 | 09:00–11:00 | Sí | 08:00 < 11:00 y 09:00 < 10:00 |
| 08:00–12:00 | 09:00–10:00 | Sí | la nueva queda dentro |
| 08:00–10:00 | 10:00–12:00 | No | 10:00 < 10:00 es falso (son contiguas) |
| 08:00–10:00 | 07:00–08:00 | No | 08:00 < 08:00 es falso |

✅ **Verifica** (con el entorno activo, en la carpeta del proyecto):

```bash
python -c "from validaciones import se_cruzan; print(se_cruzan('08:00','10:00','09:00','11:00'), se_cruzan('08:00','10:00','10:00','12:00'))"
```
Debe imprimir `True False`.

💾 `git add . ; git commit -m "feat: validaciones y regla de choque de horarios"`

---

## Paso 5 — App base, plantilla y estilos (15 min)

### 5.1 `app.py` (versión inicial)

```python
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


# (AQUÍ PEGARÁS EL CÓDIGO DE LOS PASOS 6, 7, 8 Y 9)

# ----------------------------------------------------------- ARRANQUE
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
```

- `app.teardown_appcontext(close_db)` hace que Flask cierre la BD al terminar cada petición.
- El bloque `with app.app_context(): init_db()` crea las tablas al arrancar. **Siempre debe quedar al final** del archivo. En los siguientes pasos pegarás código **encima** de ese bloque, donde está el comentario.
- `debug=True` recarga el servidor al guardar y muestra los errores detallados.

### 5.2 `templates/base.html` — esqueleto común

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block titulo %}Reservas{% endblock %} | Laboratorios ISTE</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
  <header class="barra">
    <a class="logo" href="/">Reservas de Laboratorios</a>
    <nav>
      <a href="/laboratorios">Laboratorios</a>
      <a href="/reservas">Reservas</a>
      <a href="/reporte">Reporte</a>
    </nav>
  </header>

  <main class="contenedor">
    {# Mensajes después de redirigir (flash) #}
    {% for categoria, mensaje in get_flashed_messages(with_categories=true) %}
      <div class="alerta {{ categoria }}">{{ mensaje }}</div>
    {% endfor %}

    {# Errores de validación al volver a mostrar un formulario #}
    {% if errores %}
      <div class="alerta error">
        <strong>Revise los datos:</strong>
        <ul>{% for e in errores %}<li>{{ e }}</li>{% endfor %}</ul>
      </div>
    {% endif %}

    {% block contenido %}{% endblock %}
  </main>
</body>
</html>
```

**Herencia de plantillas:** las demás páginas dicen `{% extends "base.html" %}` y solo rellenan `{% block contenido %}`. El menú y los mensajes se escriben una sola vez.

Hay dos tipos de mensaje:
- **flash**: mensajes que sobreviven a una redirección (ej. "Laboratorio creado").
- **errores**: lista que pasamos directamente cuando volvemos a mostrar un formulario con datos inválidos.

### 5.3 `templates/inicio.html`

```html
{% extends "base.html" %}
{% block titulo %}Inicio{% endblock %}
{% block contenido %}
<h1>Panel principal</h1>
<div class="tarjetas">
  <div class="tarjeta"><span>Laboratorios</span><strong>{{ totales.laboratorios }}</strong></div>
  <div class="tarjeta"><span>Disponibles</span><strong>{{ totales.disponibles }}</strong></div>
  <div class="tarjeta"><span>Reservas</span><strong>{{ totales.reservas }}</strong></div>
</div>
<p class="acciones">
  <a class="btn" href="/reservas">Nueva reserva</a>
  <a class="btn sec" href="/laboratorios">Gestionar laboratorios</a>
</p>
{% endblock %}
```

### 5.4 `static/css/styles.css`

```css
*, *::before, *::after { box-sizing: border-box; }

:root {
  --primario: #0a5bd6;
  --peligro: #dc2626;
  --gris: #64748b;
  --borde: #e5e7eb;
  --fondo: #f1f5f9;
}

body { margin: 0; font-family: system-ui, sans-serif; background: var(--fondo); color: #1f2937; }

/* Barra superior */
.barra { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;
         gap: 12px; padding: 12px 24px; background: var(--primario); }
.barra a { color: #fff; text-decoration: none; }
.barra nav { display: flex; gap: 16px; }
.logo { font-weight: 700; }

.contenedor { max-width: 1000px; margin: 24px auto; padding: 0 16px; display: grid; gap: 16px; }
.panel { background: #fff; border-radius: 10px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.panel h2 { margin-top: 0; font-size: 18px; }

/* Formularios */
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
label { display: grid; gap: 4px; font-size: 14px; }
input, select { width: 100%; padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 14px; }
.filtros { display: flex; flex-wrap: wrap; gap: 12px; align-items: end; margin-bottom: 12px; }
.filtros label { min-width: 160px; }

/* Botones */
button, .btn { display: inline-block; padding: 8px 14px; border: 0; border-radius: 6px; cursor: pointer;
               background: var(--primario); color: #fff; text-decoration: none; font-size: 14px; }
.btn.sec { background: var(--gris); }
.peligro { background: var(--peligro); }
.acciones { display: flex; gap: 8px; align-items: center; margin-top: 12px; }
td.acciones { margin: 0; }
.acciones form { margin: 0; }

/* Tablas */
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; border-bottom: 1px solid var(--borde); text-align: left; }
thead { background: #f8fafc; }
.estado { padding: 2px 8px; border-radius: 999px; font-size: 12px; }
.estado.disponible { background: #dcfce7; color: #166534; }
.estado.mantenimiento { background: #fee2e2; color: #991b1b; }

/* Mensajes */
.alerta { padding: 10px 14px; border-radius: 8px; }
.alerta ul { margin: 6px 0 0; }
.alerta.ok { background: #dcfce7; color: #166534; }
.alerta.error { background: #fee2e2; color: #991b1b; }

/* Tarjetas del inicio */
.tarjetas { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
.tarjeta { background: #fff; border-radius: 10px; padding: 16px; display: grid; gap: 4px; }
.tarjeta span { color: var(--gris); font-size: 13px; }
.tarjeta strong { font-size: 28px; }

/* Celular: la tabla se desplaza horizontalmente */
@media (max-width: 700px) {
  .panel { overflow-x: auto; }
}
```

> Si vas corto de tiempo, copia solo las secciones de body, barra, contenedor, panel, formularios, botones, tablas y mensajes. El resto es opcional.

### ▶ Ejecutar

```bash
python app.py
```
Abre **http://127.0.0.1:5000**.

✅ **Verifica:** ves el panel con **3 laboratorios, 2 disponibles, 0 reservas**, y se creó el archivo `reservas.db`. Los enlaces del menú todavía dan 404 porque esas rutas aún no existen.

Detén el servidor con `Ctrl + C` cuando lo necesites. Con `debug=True` normalmente no hace falta: se recarga solo al guardar.

💾 `git add . ; git commit -m "feat: app base con plantilla y estilos"`

---

## Paso 6 — CRUD de laboratorios (25 min)

### 6.1 Rutas: pega este bloque en `app.py` **encima** del bloque `ARRANQUE`

```python
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
```

**Cómo funciona el flujo (patrón POST → Redirect → GET):**
```
Usuario envía el formulario  ──POST /laboratorios──►  crear_laboratorio()
                                                         │
                         ┌──── ¿hay errores? ────────────┤
                         ▼ sí                            ▼ no
          vuelve a mostrar la página con         INSERT + commit + flash
          los datos escritos y los errores       redirect a /laboratorios (GET)
          (código 400)                           → si el usuario refresca, NO se duplica
```

- `request.form` contiene lo que envió el formulario (siempre texto).
- `request.args` contiene lo que va en la URL (`?editar=2`).
- `url_for("laboratorios")` genera la URL a partir del **nombre de la función**. Si cambias la URL, no se rompen los enlaces.
- Para editar reutilizamos el mismo formulario: si `form.id` existe, el `action` apunta a `/laboratorios/<id>`.

### 6.2 `templates/laboratorios.html`

```html
{% extends "base.html" %}
{% block titulo %}Laboratorios{% endblock %}
{% block contenido %}
<section class="panel">
  {# Si form.id existe estamos editando; si no, creando #}
  <h2>{{ "Editar laboratorio " ~ form.codigo if form.id else "Nuevo laboratorio" }}</h2>
  <form method="post"
        action="{{ url_for('actualizar_laboratorio', lab_id=form.id) if form.id else url_for('crear_laboratorio') }}">
    <div class="grid">
      <label>Código
        <input name="codigo" value="{{ form.codigo or '' }}" placeholder="LAB-004" required>
      </label>
      <label>Nombre
        <input name="nombre" value="{{ form.nombre or '' }}" required minlength="3">
      </label>
      <label>Piso
        <input name="piso" type="number" min="0" value="{{ form.piso if form.piso is not none else '' }}" required>
      </label>
      <label>Capacidad
        <input name="capacidad" type="number" min="1" value="{{ form.capacidad or '' }}" required>
      </label>
      <label>Estado
        <select name="estado">
          {% for e in ["disponible", "mantenimiento"] %}
            <option value="{{ e }}" {{ "selected" if form.estado == e }}>{{ e|capitalize }}</option>
          {% endfor %}
        </select>
      </label>
    </div>
    <div class="acciones">
      <button type="submit">Guardar</button>
      {% if form.id %}<a class="btn sec" href="{{ url_for('laboratorios') }}">Cancelar</a>{% endif %}
    </div>
  </form>
</section>

<section class="panel">
  <h2>Listado</h2>
  <table>
    <thead>
      <tr><th>Código</th><th>Nombre</th><th>Piso</th><th>Capacidad</th><th>Estado</th><th>Acciones</th></tr>
    </thead>
    <tbody>
    {% for lab in labs %}
      <tr>
        <td>{{ lab.codigo }}</td>
        <td>{{ lab.nombre }}</td>
        <td>{{ lab.piso }}</td>
        <td>{{ lab.capacidad }}</td>
        <td><span class="estado {{ lab.estado }}">{{ lab.estado }}</span></td>
        <td class="acciones">
          <a class="btn sec" href="{{ url_for('laboratorios', editar=lab.id) }}">Editar</a>
          <form method="post" action="{{ url_for('eliminar_laboratorio', lab_id=lab.id) }}"
                onsubmit="return confirm('¿Eliminar {{ lab.codigo }}?')">
            <button class="peligro">Eliminar</button>
          </form>
        </td>
      </tr>
    {% else %}
      <tr><td colspan="6">No hay laboratorios registrados.</td></tr>
    {% endfor %}
    </tbody>
  </table>
</section>
{% endblock %}
```

- `{% for ... %}{% else %}{% endfor %}`: el `else` se muestra si la lista está vacía.
- Eliminar es un `<form method="post">` y no un enlace. Nunca borres con GET, porque un buscador o una precarga del navegador podría borrar datos.
- `onsubmit="return confirm(...)"` pide confirmación.

✅ **Verifica** en http://127.0.0.1:5000/laboratorios:

| Prueba | Resultado esperado |
|---|---|
| Crear `lab-004`, "Lab Hardware", piso 1, capacidad 20 | Aparece como **LAB-004** y el mensaje verde |
| Crear otro con código `LAB-001` | Error "Ya existe un laboratorio..." y los datos siguen escritos |
| Capacidad 0 | Error de capacidad (quita temporalmente `min="1"` del HTML para probar la validación del servidor) |
| Editar LAB-004, cambiar el nombre | Se actualiza |
| Eliminar LAB-004 | Desaparece |

💾 `git add . ; git commit -m "feat: CRUD de laboratorios"`

---

## Paso 7 — Reservas y filtros (25 min)

### 7.1 Rutas: pega en `app.py` **encima** del bloque `ARRANQUE`

```python
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
```

- **JOIN**: trae el nombre del laboratorio junto a cada reserva.
- **Filtros dinámicos**: empezamos con `WHERE 1 = 1` (siempre verdadero) para poder añadir `AND ...` solo si el usuario llenó el filtro, y los valores van en `params`, nunca pegados al SQL.

### 7.2 `templates/reservas.html`

```html
{% extends "base.html" %}
{% block titulo %}Reservas{% endblock %}
{% block contenido %}
<section class="panel">
  <h2>Nueva reserva</h2>
  <form method="post" action="{{ url_for('crear_reserva') }}">
    <div class="grid">
      <label>Docente
        <input name="docente" value="{{ form.docente or '' }}" required>
      </label>
      <label>Laboratorio
        <select name="laboratorio_id" required>
          <option value="">-- Seleccione --</option>
          {% for lab in labs %}
            <option value="{{ lab.id }}"
                    {{ "selected" if (form.laboratorio_id|string) == (lab.id|string) }}
                    {{ "disabled" if lab.estado == "mantenimiento" }}>
              {{ lab.codigo }} - {{ lab.nombre }}{{ " (mantenimiento)" if lab.estado == "mantenimiento" }}
            </option>
          {% endfor %}
        </select>
      </label>
      <label>Fecha
        <input name="fecha" type="date" value="{{ form.fecha or '' }}" required>
      </label>
      <label>Hora inicio
        <input name="hora_inicio" type="time" value="{{ form.hora_inicio or '' }}" required>
      </label>
      <label>Hora fin
        <input name="hora_fin" type="time" value="{{ form.hora_fin or '' }}" required>
      </label>
      <label>Motivo
        <input name="motivo" value="{{ form.motivo or '' }}">
      </label>
    </div>
    <div class="acciones"><button type="submit">Reservar</button></div>
  </form>
</section>

<section class="panel">
  <h2>Reservas registradas</h2>
  {# Filtros: formulario GET → los valores viajan en la URL (?fecha=...&lab=...) #}
  <form method="get" class="filtros">
    <label>Fecha <input name="fecha" type="date" value="{{ filtro.fecha }}"></label>
    <label>Laboratorio
      <select name="lab">
        <option value="">Todos</option>
        {% for lab in labs %}
          <option value="{{ lab.id }}" {{ "selected" if filtro.lab == lab.id|string }}>{{ lab.codigo }}</option>
        {% endfor %}
      </select>
    </label>
    <button type="submit">Filtrar</button>
    <a class="btn sec" href="{{ url_for('reservas') }}">Limpiar</a>
  </form>

  <table>
    <thead>
      <tr><th>Fecha</th><th>Horario</th><th>Laboratorio</th><th>Docente</th><th>Motivo</th><th></th></tr>
    </thead>
    <tbody>
    {% for r in reservas %}
      <tr>
        <td>{{ r.fecha }}</td>
        <td>{{ r.hora_inicio }} - {{ r.hora_fin }}</td>
        <td>{{ r.codigo }} - {{ r.laboratorio }}</td>
        <td>{{ r.docente }}</td>
        <td>{{ r.motivo or "" }}</td>
        <td>
          <form method="post" action="{{ url_for('eliminar_reserva', reserva_id=r.id) }}"
                onsubmit="return confirm('¿Cancelar esta reserva?')">
            <button class="peligro">Cancelar</button>
          </form>
        </td>
      </tr>
    {% else %}
      <tr><td colspan="6">No hay reservas.</td></tr>
    {% endfor %}
    </tbody>
  </table>
</section>
{% endblock %}
```

- `disabled` en los laboratorios en mantenimiento es una ayuda visual. **La validación real está en el servidor**, porque cualquiera puede enviar el formulario saltándose el HTML.
- `|string` en Jinja convierte a texto para comparar: el formulario envía `"2"` y la BD tiene `2`.
- El formulario de filtros usa `method="get"`, así que los filtros quedan en la URL y se pueden compartir.

✅ **Verifica** en http://127.0.0.1:5000/reservas (usa el mismo laboratorio y fecha):

| Reserva | Esperado |
|---|---|
| LAB-002, 08:00–10:00 | ✔ Registrada |
| LAB-002, 09:00–11:00 | ✘ "Horario ocupado: 08:00-10:00..." |
| LAB-002, 10:00–12:00 | ✔ (contigua) |
| LAB-001, 08:00–10:00 | ✔ (otro laboratorio) |
| Hora fin 07:00 con inicio 09:00 | ✘ "La hora de fin debe ser mayor..." |
| Filtrar por fecha / laboratorio | Solo aparecen las que coinciden |
| Eliminar LAB-002 en /laboratorios | ✘ "tiene reservas registradas" |

💾 `git add . ; git commit -m "feat: reservas con validación de choques y filtros"`

---

## Paso 8 — Reporte (7 min)

### 8.1 Ruta: pega en `app.py` **encima** del bloque `ARRANQUE`

```python
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
```

- **LEFT JOIN**: incluye los laboratorios **sin** reservas (con 0).
- `strftime('%s', hora)` convierte la hora a segundos, y al dividir para 3600 obtienes horas.
- `COALESCE(x, 0)`: si no hay reservas, `SUM` da NULL y lo convertimos en 0.
- En **MySQL** sería: `SUM(TIME_TO_SEC(TIMEDIFF(r.hora_fin, r.hora_inicio)) / 3600)`.

### 8.2 `templates/reporte.html`

```html
{% extends "base.html" %}
{% block titulo %}Reporte{% endblock %}
{% block contenido %}
<section class="panel">
  <h2>Uso de laboratorios</h2>
  <table>
    <thead><tr><th>Código</th><th>Laboratorio</th><th>Reservas</th><th>Horas reservadas</th></tr></thead>
    <tbody>
    {% for f in filas %}
      <tr>
        <td>{{ f.codigo }}</td>
        <td>{{ f.nombre }}</td>
        <td>{{ f.total_reservas }}</td>
        <td>{{ f.horas }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</section>
{% endblock %}
```

✅ **Verifica:** con una reserva de 08:00 a 10:00, el reporte muestra 1 reserva y 2.0 horas.

💾 `git add . ; git commit -m "feat: reporte de uso por laboratorio"`

---

## Paso 9 — API REST en JSON (7 min)

Pega en `app.py` **encima** del bloque `ARRANQUE`:

```python
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
```

✅ **Verifica:**
- En el navegador: http://127.0.0.1:5000/api/laboratorios muestra el JSON.
- Crear por API desde **PowerShell**:
  ```powershell
  Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/laboratorios -ContentType "application/json" -Body '{"codigo":"LAB-050","nombre":"Lab API","piso":1,"capacidad":12}'
  ```
- Desde **CMD / Git Bash / Linux**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/laboratorios -H "Content-Type: application/json" -d "{\"codigo\":\"LAB-051\",\"nombre\":\"Lab API\",\"piso\":1,\"capacidad\":12}"
  ```
  Respuesta esperada: código **201** con el laboratorio creado. Si envías `{}`, la respuesta es **400** con la lista de errores.

💾 `git add . ; git commit -m "feat: API JSON de laboratorios y reservas"`

---

## Paso 10 — Pruebas automáticas (8 min)

### `tests/test_app.py`

```python
"""Pruebas. Ejecutar desde la carpeta del proyecto:  python -m unittest discover tests -v"""
import os
import tempfile
import unittest

from app import app
from db import init_db
from validaciones import se_cruzan


class TestReglas(unittest.TestCase):
    """Pruebas unitarias: la función pura, sin base de datos."""

    def test_horarios_que_se_cruzan(self):
        self.assertTrue(se_cruzan("08:00", "10:00", "09:00", "11:00"))
        self.assertTrue(se_cruzan("08:00", "12:00", "09:00", "10:00"))   # uno dentro del otro

    def test_horarios_contiguos_no_se_cruzan(self):
        self.assertFalse(se_cruzan("08:00", "10:00", "10:00", "12:00"))


class TestApp(unittest.TestCase):
    """Pruebas de integración: peticiones HTTP reales contra una BD temporal."""

    def setUp(self):
        self.fd, self.ruta = tempfile.mkstemp(suffix=".db")
        app.config.update(TESTING=True, DATABASE=self.ruta)
        with app.app_context():
            init_db()
        self.client = app.test_client()

    def tearDown(self):
        os.close(self.fd)
        os.remove(self.ruta)

    def reservar(self, inicio, fin, lab=2, fecha="2026-09-25"):
        return self.client.post("/reservas", data={
            "docente": "Ing. Ruiz", "laboratorio_id": lab, "fecha": fecha,
            "hora_inicio": inicio, "hora_fin": fin, "motivo": "Clase"})

    def test_paginas_cargan(self):
        for ruta in ["/", "/laboratorios", "/reservas", "/reporte", "/laboratorios?editar=1"]:
            self.assertEqual(self.client.get(ruta).status_code, 200, ruta)

    def test_crear_laboratorio(self):
        r = self.client.post("/laboratorios", data={
            "codigo": "lab-010", "nombre": "Lab IA", "piso": "3", "capacidad": "15", "estado": "disponible"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("LAB-010", self.client.get("/laboratorios").get_data(as_text=True))

    def test_laboratorio_invalido_y_duplicado(self):
        r = self.client.post("/laboratorios", data={"codigo": "LAB-001", "nombre": "X", "piso": "-1",
                                                    "capacidad": "0", "estado": "otro"})
        self.assertEqual(r.status_code, 400)
        html = r.get_data(as_text=True)
        self.assertIn("Ya existe", html)
        self.assertIn("capacidad", html)

    def test_editar_laboratorio(self):
        r = self.client.post("/laboratorios/1", data={
            "codigo": "LAB-001", "nombre": "Redes Renovado", "piso": "1", "capacidad": "40",
            "estado": "disponible"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("Redes Renovado", self.client.get("/laboratorios").get_data(as_text=True))

    def test_reserva_valida(self):
        self.assertEqual(self.reservar("08:00", "10:00").status_code, 302)

    def test_reserva_que_choca(self):
        self.reservar("08:00", "10:00")
        r = self.reservar("09:00", "11:00")
        self.assertEqual(r.status_code, 400)
        self.assertIn("Horario ocupado", r.get_data(as_text=True))

    def test_reservas_contiguas_y_otro_dia(self):
        self.reservar("08:00", "10:00")
        self.assertEqual(self.reservar("10:00", "12:00").status_code, 302)
        self.assertEqual(self.reservar("08:00", "10:00", fecha="2026-09-26").status_code, 302)

    def test_hora_fin_menor(self):
        self.assertEqual(self.reservar("10:00", "09:00").status_code, 400)

    def test_laboratorio_en_mantenimiento(self):
        self.assertEqual(self.reservar("08:00", "09:00", lab=3).status_code, 400)

    def test_no_elimina_laboratorio_con_reservas(self):
        self.reservar("08:00", "10:00")
        self.client.post("/laboratorios/2/eliminar")
        self.assertEqual(len(self.client.get("/api/laboratorios").get_json()), 3)
        self.client.post("/laboratorios/1/eliminar")                 # este no tiene reservas
        self.assertEqual(len(self.client.get("/api/laboratorios").get_json()), 2)

    def test_filtro_y_reporte(self):
        self.reservar("08:00", "10:30")
        self.reservar("08:00", "09:00", fecha="2026-09-26")
        self.assertEqual(len(self.client.get("/api/reservas?fecha=2026-09-26").get_json()), 1)
        self.assertIn("3.5", self.client.get("/reporte").get_data(as_text=True))

    def test_api_crear(self):
        r = self.client.post("/api/laboratorios", json={"codigo": "LAB-020", "nombre": "Lab Móvil",
                                                         "piso": 1, "capacidad": 10})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["codigo"], "LAB-020")
        self.assertEqual(self.client.post("/api/laboratorios", json={}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
```

- **Pruebas unitarias** (`TestReglas`): prueban una función sola, sin BD.
- **Pruebas de integración** (`TestApp`): hacen peticiones reales con `app.test_client()` contra una **BD temporal**, así que no ensucian tu `reservas.db`.
- `setUp` corre antes de **cada** prueba y `tearDown` después, así que cada prueba empieza con datos limpios.

```bash
python -m unittest discover tests -v
```

✅ **Verifica:** `Ran 14 tests ... OK`

💾 `git add . ; git commit -m "test: pruebas unitarias y de integración"`

---

## Paso 11 — README y GitHub (10 min)

### `README.md`

````markdown
# Sistema de Reserva de Laboratorios (Flask)

Aplicación web para registrar laboratorios y gestionar sus reservas, evitando choques de horario.

## Funcionalidades
- CRUD de laboratorios (código único, piso, capacidad, estado).
- Reservas con validaciones: horario válido, laboratorio disponible y **sin cruces de horario**.
- Listado de reservas con filtros por fecha y laboratorio.
- Reporte de reservas y horas por laboratorio.
- API REST: `GET/POST /api/laboratorios`, `GET /api/reservas?fecha=AAAA-MM-DD`.

## Tecnologías
Python 3, Flask, SQLite, Jinja2, HTML/CSS.

## Instalación y ejecución
```bash
python -m venv venv
venv\Scripts\activate            # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Abrir http://127.0.0.1:5000. La base de datos `reservas.db` se crea automáticamente con 3 laboratorios de ejemplo.

## Pruebas
```bash
python -m unittest discover tests -v
```

## Estructura
```
app.py            Rutas (controladores)
db.py             Conexión e inicialización de la BD
schema.sql        Tablas
validaciones.py   Reglas de negocio
templates/        Vistas HTML (Jinja2)
static/css/       Estilos
tests/            Pruebas automáticas
```
````

### Subir a GitHub
1. En github.com: **New repository**, con el nombre `reservas-flask`, **sin** README (ya lo tienes). Pulsa Create.
2. En la terminal:
   ```bash
   git add . ; git commit -m "docs: README con instrucciones"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/reservas-flask.git
   git push -u origin main
   ```
3. Si pide contraseña, usa un **token** (GitHub → Settings → Developer settings → Personal access tokens), no tu contraseña normal.

✅ **Verifica:** `git log --oneline` muestra unos 9 commits con mensajes claros.

---

## Paso 12 — Revisión final (últimos 15–20 min de la prueba)

- [ ] Borra `reservas.db`, ejecuta `python app.py` y confirma que todo se crea solo.
- [ ] Recorre todas las pantallas como si fueras el evaluador.
- [ ] Envía formularios vacíos: ninguno debe dar error 500.
- [ ] Revisa los casos de choque de la tabla del Paso 7.
- [ ] El README explica cómo ejecutarlo.
- [ ] `git status` limpio y último commit hecho.

## Errores comunes y solución

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask'` | El entorno virtual no está activo | `venv\Scripts\activate` |
| `TemplateNotFound: laboratorios.html` | El archivo no está en `templates/` o tiene otro nombre | Revisa la carpeta y el nombre exacto |
| `BuildError: Could not build url for endpoint 'x'` | `url_for('x')` apunta a una función que no existe o tiene otro nombre | Revisa el nombre de la función |
| `sqlite3.OperationalError: no such table` | Cambiaste el esquema o la BD quedó a medias | Detén el servidor, borra `reservas.db` y vuelve a ejecutar |
| `sqlite3.IntegrityError: UNIQUE constraint failed` | Faltó validar el duplicado antes del INSERT | Revisa `validar_laboratorio` |
| `KeyError: 'nombre'` en `request.form[...]` | El `name` del input no coincide | Compara el `name=""` del HTML con el código |
| `werkzeug ... 405 Method Not Allowed` | El formulario hace POST a una ruta que solo acepta GET (o al revés) | Revisa `method=` y `@app.post`/`@app.get` |
| Los estilos no cargan | Ruta incorrecta | Debe ser `static/css/styles.css` y usar `url_for('static', filename='css/styles.css')` |
| `Address already in use` | Ya hay un servidor corriendo | Cierra la otra terminal o usa `app.run(debug=True, port=5001)` |

## Si en el laboratorio te piden MySQL en vez de SQLite

1. `pip install mysql-connector-python`
2. En `db.py` cambia la conexión:
   ```python
   import mysql.connector
   g.db = mysql.connector.connect(host="localhost", user="root", password="", database="reservas")
   cursor = g.db.cursor(dictionary=True)
   ```
3. En las consultas, los parámetros son `%s` en lugar de `?`, y se ejecutan con un cursor: `cur.execute(sql, params)` y luego `cur.fetchall()`.
4. En `schema.sql` cambia `INTEGER PRIMARY KEY AUTOINCREMENT` por `INT AUTO_INCREMENT PRIMARY KEY`, `TEXT` por `VARCHAR(100)`, y usa los tipos `DATE` y `TIME`.

## Cómo explicarle tu proyecto al evaluador (30 segundos)

> "Separé el proyecto en capas: `schema.sql` y `db.py` para los datos, `validaciones.py` para las reglas de negocio y `app.py` para las rutas, con plantillas Jinja que heredan de una base. Todas las consultas son parametrizadas para evitar SQL Injection. Valido en el servidor, no solo en el HTML. Para los choques de horario uso la condición de intervalos superpuestos directamente en SQL. Uso el patrón POST-Redirect-GET para no duplicar registros, y tengo pruebas unitarias y de integración con una base temporal."
