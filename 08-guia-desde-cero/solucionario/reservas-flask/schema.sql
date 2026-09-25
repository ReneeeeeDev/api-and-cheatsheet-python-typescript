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
