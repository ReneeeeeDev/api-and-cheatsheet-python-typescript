"""06 - Archivos de texto, JSON y CSV. Crea una carpeta 'salida_06' con los archivos generados.
Ejecutar:  python 06_archivos_json_csv.py
"""
import csv
import json
from pathlib import Path

carpeta = Path(__file__).parent / "salida_06"
carpeta.mkdir(exist_ok=True)

# ---------------------------------------------------------------- TEXTO
ruta_txt = carpeta / "notas.txt"
with open(ruta_txt, "w", encoding="utf-8") as f:          # "w" sobrescribe
    f.write("Ana;9.5\n")
    f.writelines(["Luis;6.8\n", "María;8.0\n"])
with open(ruta_txt, "a", encoding="utf-8") as f:          # "a" agrega al final
    f.write("Pedro;7.2\n")

with open(ruta_txt, encoding="utf-8") as f:               # "r" por defecto
    for num, linea in enumerate(f, 1):
        nombre, nota = linea.strip().split(";")
        print(num, nombre, float(nota))

print(ruta_txt.read_text(encoding="utf-8").splitlines())   # atajo con pathlib
print(ruta_txt.exists(), ruta_txt.name, ruta_txt.suffix, ruta_txt.stat().st_size, "bytes")

# ---------------------------------------------------------------- JSON
datos = {
    "instituto": "ISTE",
    "estudiantes": [
        {"nombre": "Ana", "notas": [9, 10], "activo": True},
        {"nombre": "Luis", "notas": [6, 7], "activo": False},
    ],
}
ruta_json = carpeta / "datos.json"
with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)       # ensure_ascii=False conserva tildes

with open(ruta_json, encoding="utf-8") as f:
    leido = json.load(f)
print(leido["estudiantes"][0]["nombre"], type(leido))

texto = json.dumps({"a": 1, "b": None, "c": [1, 2]})       # objeto → string
print(texto, json.loads(texto)["b"])                        # {"a": 1, "b": null, "c": [1, 2]} None

# ---------------------------------------------------------------- CSV
ruta_csv = carpeta / "productos.csv"
productos = [
    {"codigo": "P01", "nombre": "Mouse", "precio": 12.5, "stock": 10},
    {"codigo": "P02", "nombre": "Teclado, mecánico", "precio": 45, "stock": 3},   # coma dentro: csv la entrecomilla
    {"codigo": "P03", "nombre": "Monitor", "precio": 139.99, "stock": 0},
]
with open(ruta_csv, "w", newline="", encoding="utf-8") as f:   # newline="" evita líneas en blanco en Windows
    escritor = csv.DictWriter(f, fieldnames=["codigo", "nombre", "precio", "stock"])
    escritor.writeheader()
    escritor.writerows(productos)

with open(ruta_csv, newline="", encoding="utf-8") as f:
    lector = csv.DictReader(f)                 # cada fila es un diccionario (¡valores como texto!)
    filas = list(lector)
valor_inventario = sum(float(r["precio"]) * int(r["stock"]) for r in filas)
sin_stock = [r["nombre"] for r in filas if int(r["stock"]) == 0]
print(len(filas), "productos | valor:", round(valor_inventario, 2), "| sin stock:", sin_stock)

# CSV con punto y coma (Excel en español suele usar ;)
with open(carpeta / "excel.csv", "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig: Excel ve bien las tildes
    w = csv.writer(f, delimiter=";")
    w.writerow(["Nombre", "Nota"])
    w.writerows([["Ana", 9.5], ["Luis", 6.8]])

# ---------------------------------------------------------------- MANEJO DE ERRORES CON ARCHIVOS
try:
    open(carpeta / "no_existe.txt", encoding="utf-8")
except FileNotFoundError:
    print("El archivo no existe")

# Listar archivos de una carpeta
for archivo in sorted(carpeta.iterdir()):
    print(" -", archivo.name)
print(list(carpeta.glob("*.csv")))
