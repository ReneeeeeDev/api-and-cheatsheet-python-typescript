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
