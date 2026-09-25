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
