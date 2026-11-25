# Práctica de SQL

| Archivo | Contenido |
|---|---|
| `practica.sql` | Esquema instituto (carreras, estudiantes, materias, notas) + **15 ejercicios** resueltos (SQLite) |
| `practica_mysql.sql` | Lo mismo adaptado a **MySQL/XAMPP** (AUTO_INCREMENT, FOREIGN KEY explícitas) |
| `ejercicios_extra.sql` | Facturación + mesa de ayuda TI: **25 ejercicios** (16–40) con JOIN múltiples, LEFT JOIN con filtros, pivot, CTE, funciones de ventana, subconsultas correlacionadas, UPDATE con subconsulta, transacciones y vistas |
| `ejecutar_sql.py` | Ejecuta cualquier `.sql` y muestra los resultados como tablas, sin instalar nada |

## Ejecutar
```bash
python ejecutar_sql.py practica.sql
python ejecutar_sql.py ejercicios_extra.sql
python ejecutar_sql.py ejercicios_extra.sql --db tienda.db   # guarda la base para seguir consultando
python ejecutar_sql.py --db tienda.db                         # consola interactiva (.tables, .schema, .salir)
```
MySQL: phpMyAdmin → crear base → pestaña SQL → pegar `practica_mysql.sql`.

## Cómo practicar
1. Ejecuta el archivo una vez para crear las tablas: `python ejecutar_sql.py ejercicios_extra.sql --db practica.db`.
2. Abre la consola: `python ejecutar_sql.py --db practica.db`.
3. Lee el enunciado de cada ejercicio (línea `-- N.`), escribe tu consulta y compárala con la solución que está debajo.
