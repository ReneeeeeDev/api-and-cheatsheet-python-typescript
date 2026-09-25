"""02 - Listas, tuplas, diccionarios, sets, comprehensions y ordenamiento.
Ejecutar:  python 02_colecciones.py
"""
from collections import Counter, defaultdict

# ---------------------------------------------------------------- LISTAS
nums = [5, 3, 8, 1]
nums.append(10)          # [5, 3, 8, 1, 10]
nums.insert(0, 99)       # [99, 5, 3, 8, 1, 10]
nums.extend([7, 7])      # agrega varios
nums.remove(7)           # quita el PRIMER 7
ultimo = nums.pop()      # quita y devuelve el último
primero = nums.pop(0)    # quita y devuelve el índice 0
print(nums, ultimo, primero)                    # [5, 3, 8, 1, 10] 7 99

print(nums[0], nums[-1], nums[1:3], nums[:2], nums[::-1])   # 5 10 [3, 8] [5, 3] [10, 1, 8, 3, 5]
print(len(nums), sum(nums), max(nums), min(nums), 8 in nums, nums.index(8), nums.count(3))

ordenada = sorted(nums)                  # NUEVA lista ordenada
nums.sort(reverse=True)                  # ordena la MISMA lista
print(ordenada, nums)

copia = nums[:]                          # copia superficial (también list(nums) o nums.copy())
copia.append(0)
print(len(nums) != len(copia))           # True: son listas distintas

# Matriz (lista de listas)
matriz = [[1, 2, 3], [4, 5, 6]]
print(matriz[1][2])                                       # 6
print([fila[0] for fila in matriz])                       # columna 0: [1, 4]
print([list(col) for col in zip(*matriz)])                # transpuesta: [[1, 4], [2, 5], [3, 6]]

# ---------------------------------------------------------------- COMPREHENSIONS
pares = [x for x in range(10) if x % 2 == 0]              # [0, 2, 4, 6, 8]
cuadrados = {x: x ** 2 for x in range(1, 5)}              # {1: 1, 2: 4, 3: 9, 4: 16}
letras = {c for c in "banana"}                            # {'a', 'b', 'n'}
etiquetas = ["par" if x % 2 == 0 else "impar" for x in range(4)]
print(pares, cuadrados, sorted(letras), etiquetas)

# ---------------------------------------------------------------- TUPLAS (inmutables)
punto = (3, 4)
x, y = punto                          # desempaquetado
print(x, y, punto[0])
# punto[0] = 9  → TypeError
primero, *resto = [1, 2, 3, 4]
print(primero, resto)                 # 1 [2, 3, 4]

# ---------------------------------------------------------------- DICCIONARIOS
persona = {"nombre": "Ana", "edad": 25}
persona["email"] = "ana@mail.com"                 # agregar / modificar
persona.update({"edad": 26, "ciudad": "Ambato"})
print(persona.get("telefono", "N/A"))             # N/A (sin error)
print(persona.pop("ciudad"), "edad" in persona)   # Ambato True
for clave, valor in persona.items():
    print(f"  {clave}: {valor}")
print(list(persona.keys()), list(persona.values()))

# Contar con diccionario (3 formas)
texto = "el perro y el gato y el loro"
conteo = {}
for p in texto.split():
    conteo[p] = conteo.get(p, 0) + 1
print(conteo)
print(Counter(texto.split()).most_common(2))      # [('el', 3), ('y', 2)]

# Agrupar
ventas = [("Quito", 100), ("Ambato", 50), ("Quito", 30)]
por_ciudad = defaultdict(list)
for ciudad, monto in ventas:
    por_ciudad[ciudad].append(monto)
print(dict(por_ciudad), {c: sum(m) for c, m in por_ciudad.items()})

# ---------------------------------------------------------------- LISTA DE DICCIONARIOS (típico CRUD)
estudiantes = [
    {"id": 1, "nombre": "Ana", "nota": 9.0, "carrera": "Software"},
    {"id": 2, "nombre": "Luis", "nota": 6.5, "carrera": "Software"},
    {"id": 3, "nombre": "María", "nota": 8.0, "carrera": "Enfermería"},
]
aprobados = [e["nombre"] for e in estudiantes if e["nota"] >= 7]
promedio = sum(e["nota"] for e in estudiantes) / len(estudiantes)
mejor = max(estudiantes, key=lambda e: e["nota"])
por_nota = sorted(estudiantes, key=lambda e: (-e["nota"], e["nombre"]))
print(aprobados, round(promedio, 2), mejor["nombre"], [e["nombre"] for e in por_nota])
# ['Ana', 'María'] 7.83 Ana ['Ana', 'María', 'Luis']

# "CRUD" en memoria
def buscar(id_):
    return next((e for e in estudiantes if e["id"] == id_), None)

buscar(2)["nota"] = 7.0                                   # actualizar
estudiantes = [e for e in estudiantes if e["id"] != 3]    # eliminar
estudiantes.append({"id": 4, "nombre": "Pedro", "nota": 8.5, "carrera": "Marketing"})  # crear
print([(e["id"], e["nombre"], e["nota"]) for e in estudiantes])

# ---------------------------------------------------------------- SETS (sin repetidos)
a, b = {1, 2, 3, 4}, {3, 4, 5}
print(a & b, a | b, a - b, a ^ b)          # {3, 4} {1, 2, 3, 4, 5} {1, 2} {1, 2, 5}
print(list(dict.fromkeys([3, 1, 3, 2])))   # quitar duplicados CONSERVANDO orden: [3, 1, 2]

# ---------------------------------------------------------------- FUNCIONES ÚTILES
nombres = ["Ana", "Luis", "María"]
notas = [9, 6, 8]
for i, n in enumerate(nombres, start=1):
    print(i, n)
for n, nt in zip(nombres, notas):
    print(n, nt)
print(any(n < 7 for n in notas), all(n > 5 for n in notas))   # True True
print(list(map(str.upper, nombres)), list(filter(lambda n: n > 7, notas)))
