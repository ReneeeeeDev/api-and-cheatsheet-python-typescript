"""07 - CRUD completo por consola con SQLite (sin librerías externas).
Incluye: crear tablas con FK, insertar, consultar con JOIN/GROUP BY, actualizar, eliminar,
transacciones y protección contra SQL Injection.
Ejecutar:  python 07_sqlite_crud.py           (demostración automática)
           python 07_sqlite_crud.py menu      (menú interactivo)
"""
import sqlite3
import sys
from pathlib import Path

RUTA_DB = Path(__file__).parent / "biblioteca.db"


def conectar():
    con = sqlite3.connect(RUTA_DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def crear_tablas(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        pais TEXT
    );
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        anio INTEGER CHECK (anio > 0),
        stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
        autor_id INTEGER NOT NULL REFERENCES autores(id) ON DELETE CASCADE
    );
    """)


# ---------------------------------------------------------------- CRUD
def crear_autor(con, nombre, pais):
    cur = con.execute("INSERT INTO autores (nombre, pais) VALUES (?, ?)", (nombre, pais))
    con.commit()
    return cur.lastrowid


def crear_libro(con, titulo, anio, stock, autor_id):
    cur = con.execute("INSERT INTO libros (titulo, anio, stock, autor_id) VALUES (?, ?, ?, ?)",
                      (titulo, anio, stock, autor_id))
    con.commit()
    return cur.lastrowid


def listar_libros(con, texto=""):
    return con.execute("""
        SELECT l.id, l.titulo, l.anio, l.stock, a.nombre AS autor
        FROM libros l JOIN autores a ON a.id = l.autor_id
        WHERE l.titulo LIKE ? OR a.nombre LIKE ?
        ORDER BY l.titulo""", (f"%{texto}%", f"%{texto}%")).fetchall()


def obtener_libro(con, id_):
    return con.execute("SELECT * FROM libros WHERE id = ?", (id_,)).fetchone()


def actualizar_stock(con, id_, stock):
    cur = con.execute("UPDATE libros SET stock = ? WHERE id = ?", (stock, id_))
    con.commit()
    return cur.rowcount                     # filas afectadas (0 = no existía)


def eliminar_libro(con, id_):
    cur = con.execute("DELETE FROM libros WHERE id = ?", (id_,))
    con.commit()
    return cur.rowcount > 0


def resumen_por_autor(con):
    return con.execute("""
        SELECT a.nombre, COUNT(l.id) AS libros, COALESCE(SUM(l.stock), 0) AS unidades
        FROM autores a LEFT JOIN libros l ON l.autor_id = a.id
        GROUP BY a.id ORDER BY unidades DESC""").fetchall()


def prestar(con, libro_id, cantidad):
    """Transacción: todo o nada."""
    try:
        with con:                            # commit automático; rollback si hay excepción
            libro = obtener_libro(con, libro_id)
            if libro is None:
                raise ValueError("Libro no existe")
            if libro["stock"] < cantidad:
                raise ValueError("Stock insuficiente")
            con.execute("UPDATE libros SET stock = stock - ? WHERE id = ?", (cantidad, libro_id))
        return True
    except ValueError as e:
        print("  No se pudo prestar:", e)
        return False


def imprimir(filas):
    if not filas:
        print("  (sin resultados)")
        return
    columnas = filas[0].keys()
    print("  " + " | ".join(f"{c:<22}" for c in columnas))
    for f in filas:
        print("  " + " | ".join(f"{str(f[c]):<22}" for c in columnas))


def demo():
    if RUTA_DB.exists():
        RUTA_DB.unlink()                      # empezar limpio
    con = conectar()
    crear_tablas(con)
    gg = crear_autor(con, "Gabriel García Márquez", "Colombia")
    ji = crear_autor(con, "Jorge Icaza", "Ecuador")
    crear_autor(con, "Autor Sin Libros", "Perú")
    crear_libro(con, "Cien años de soledad", 1967, 5, gg)
    crear_libro(con, "El amor en los tiempos del cólera", 1985, 2, gg)
    h = crear_libro(con, "Huasipungo", 1934, 3, ji)

    print("\n== Todos los libros");            imprimir(listar_libros(con))
    print("\n== Buscar 'icaza'");              imprimir(listar_libros(con, "icaza"))
    print("\n== Actualizar stock de Huasipungo a 10 → filas:", actualizar_stock(con, h, 10))
    print("== Actualizar id 999 → filas:", actualizar_stock(con, 999, 1))
    print("\n== Préstamo de 4 (ok):", prestar(con, h, 4))
    print("== Préstamo de 50:", prestar(con, h, 50))
    print("\n== Resumen por autor (LEFT JOIN + GROUP BY)"); imprimir(resumen_por_autor(con))
    print("\n== Eliminar libro 1:", eliminar_libro(con, 1))
    print("== Eliminar libro 1 otra vez:", eliminar_libro(con, 1))

    try:
        crear_autor(con, "Jorge Icaza", "Ecuador")
    except sqlite3.IntegrityError as e:
        print("\n== Error esperado por UNIQUE:", e)

    # SQL Injection: por qué SIEMPRE usar ?
    malicioso = "x' OR '1'='1"
    inseguro = f"SELECT COUNT(*) FROM libros WHERE titulo = '{malicioso}'"
    print("\n== Consulta INSEGURA devuelve:", con.execute(inseguro).fetchone()[0], "filas (¡todas!)")
    print("== Consulta SEGURA devuelve:",
          con.execute("SELECT COUNT(*) FROM libros WHERE titulo = ?", (malicioso,)).fetchone()[0], "filas")
    con.close()
    print(f"\nBase creada en: {RUTA_DB}  (ábrela con la extensión SQLite Viewer de VS Code)")


def menu():
    con = conectar()
    crear_tablas(con)
    if not con.execute("SELECT 1 FROM autores").fetchone():
        crear_autor(con, "Anónimo", "-")
    opciones = "\n1) Listar  2) Buscar  3) Agregar libro  4) Cambiar stock  5) Eliminar  0) Salir"
    while True:
        print(opciones)
        op = input("Opción: ").strip()
        try:
            if op == "1":
                imprimir(listar_libros(con))
            elif op == "2":
                imprimir(listar_libros(con, input("Texto: ")))
            elif op == "3":
                imprimir(con.execute("SELECT id, nombre FROM autores").fetchall())
                nuevo = crear_libro(con, input("Título: "), int(input("Año: ")), int(input("Stock: ")),
                                    int(input("ID autor: ")))
                print("Creado con id", nuevo)
            elif op == "4":
                print("Filas actualizadas:", actualizar_stock(con, int(input("ID: ")), int(input("Stock: "))))
            elif op == "5":
                print("Eliminado" if eliminar_libro(con, int(input("ID: "))) else "No existe")
            elif op == "0":
                break
        except ValueError:
            print("Dato numérico inválido")
        except sqlite3.IntegrityError as e:
            print("Error de integridad:", e)
    con.close()


if __name__ == "__main__":
    menu() if len(sys.argv) > 1 and sys.argv[1] == "menu" else demo()
