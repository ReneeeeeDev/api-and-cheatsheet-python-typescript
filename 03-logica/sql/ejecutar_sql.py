"""Ejecuta archivos .sql en SQLite y muestra cada resultado como tabla (sin instalar nada).

Uso:
    python ejecutar_sql.py practica.sql              ejecuta el archivo en una BD en memoria
    python ejecutar_sql.py ejercicios_extra.sql
    python ejecutar_sql.py practica.sql --db mi.db   guarda la BD en un archivo
    python ejecutar_sql.py                           modo interactivo (escribe SQL; termina con ;)
    python ejecutar_sql.py --db mi.db                modo interactivo sobre un archivo

En modo interactivo:  .tables   .schema tabla   .salir
"""
import sqlite3
import sys


def imprimir_tabla(cursor, filas, maximo=50):
    if cursor.description is None:
        return
    columnas = [d[0] for d in cursor.description]
    datos = [["NULL" if v is None else str(v) for v in f] for f in filas[:maximo]]
    anchos = [min(40, max([len(c)] + [len(f[i]) for f in datos])) for i, c in enumerate(columnas)]
    linea = "+" + "+".join("-" * (a + 2) for a in anchos) + "+"
    print(linea)
    print("| " + " | ".join(c.ljust(a)[:a] for c, a in zip(columnas, anchos)) + " |")
    print(linea)
    for f in datos:
        print("| " + " | ".join(v.ljust(a)[:a] for v, a in zip(f, anchos)) + " |")
    print(linea)
    extra = f" (mostrando {maximo})" if len(filas) > maximo else ""
    print(f"{len(filas)} fila(s){extra}\n")


def sentencias(texto):
    """Divide el script en sentencias completas, ignorando líneas de comentario."""
    buffer = ""
    for linea in texto.splitlines():
        if linea.strip().startswith("--") and not buffer.strip():
            # comentario suelto: mostrar los títulos de ejercicio para orientarse
            if linea.strip().startswith("-- ") and linea.strip()[3:4].isdigit():
                yield ("titulo", linea.strip()[3:])
            continue
        buffer += linea + "\n"
        if sqlite3.complete_statement(buffer):
            yield ("sql", buffer.strip())
            buffer = ""
    if buffer.strip():
        yield ("sql", buffer.strip())


def ejecutar_archivo(con, ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    for tipo, contenido in sentencias(texto):
        if tipo == "titulo":
            print(f"\n=== {contenido}")
            continue
        try:
            cur = con.execute(contenido)
            filas = cur.fetchall()
            if cur.description:
                print(contenido.splitlines()[0][:100] + (" ..." if "\n" in contenido else ""))
                imprimir_tabla(cur, filas)
            elif cur.rowcount > 0 and contenido.split()[0].upper() in ("INSERT", "UPDATE", "DELETE"):
                print(f"({contenido.split()[0].upper()}: {cur.rowcount} fila(s) afectada(s))")
        except sqlite3.Error as e:
            print(f"\n*** ERROR: {e}\n    en: {contenido[:120]}\n")
    con.commit()


def interactivo(con):
    print("SQLite interactivo. Termina cada sentencia con ;   Comandos: .tables  .schema TABLA  .salir")
    buffer = ""
    while True:
        try:
            linea = input("sql> " if not buffer else "...> ")
        except (EOFError, KeyboardInterrupt):
            break
        comando = linea.strip()
        if not buffer and comando in (".salir", ".exit", ".quit"):
            break
        if not buffer and comando == ".tables":
            print([r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")])
            continue
        if not buffer and comando.startswith(".schema"):
            partes = comando.split()
            sql = "SELECT sql FROM sqlite_master WHERE type IN ('table','view')" + (" AND name = ?" if len(partes) > 1 else "")
            for (s,) in con.execute(sql, partes[1:2]):
                print(s + ";")
            continue
        buffer += linea + "\n"
        if sqlite3.complete_statement(buffer):
            try:
                cur = con.execute(buffer)
                imprimir_tabla(cur, cur.fetchall())
                con.commit()
                if cur.description is None:
                    print(f"OK ({cur.rowcount if cur.rowcount >= 0 else 0} filas afectadas)")
            except sqlite3.Error as e:
                print("ERROR:", e)
            buffer = ""


if __name__ == "__main__":
    args = sys.argv[1:]
    ruta_db = ":memory:"
    if "--db" in args:
        i = args.index("--db")
        ruta_db = args[i + 1]
        del args[i:i + 2]
    conexion = sqlite3.connect(ruta_db, isolation_level=None)   # autocommit: permite BEGIN/COMMIT en los scripts
    conexion.execute("PRAGMA foreign_keys = ON")
    if args:
        ejecutar_archivo(conexion, args[0])
        if ruta_db == ":memory:" and sys.stdin.isatty():
            print("\n¿Seguir consultando esta base? Escribe SQL (o .salir):")
            interactivo(conexion)
    else:
        interactivo(conexion)
    conexion.close()
