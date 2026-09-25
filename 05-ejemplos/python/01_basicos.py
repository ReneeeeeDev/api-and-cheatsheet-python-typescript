"""01 - Variables, tipos, operadores, entrada/salida y control de flujo.
Ejecutar:  python 01_basicos.py
"""

# ---------------------------------------------------------------- VARIABLES Y TIPOS
nombre = "Ana"          # str
edad = 25               # int
estatura = 1.65         # float
activo = True           # bool
nada = None             # NoneType

print(type(nombre), type(edad), type(estatura), type(activo), type(nada))
# <class 'str'> <class 'int'> <class 'float'> <class 'bool'> <class 'NoneType'>

# Asignación múltiple e intercambio
a, b = 1, 2
a, b = b, a
print("a =", a, "b =", b)                     # a = 2 b = 1

# ---------------------------------------------------------------- OPERADORES
print(7 + 2, 7 - 2, 7 * 2, 7 / 2)             # 9 5 14 3.5   (/ siempre da float)
print(7 // 2, 7 % 2, 2 ** 10)                 # 3 1 1024     (división entera, residuo, potencia)
print(-7 // 2)                                # -4  (redondea hacia abajo, ¡ojo!)
print(round(3.14159, 2), abs(-5), max(3, 9, 1), min(3, 9, 1))   # 3.14 5 9 1

# Comparación y lógicos
print(5 > 3 and 2 > 1, 5 > 3 or 2 > 5, not True)   # True True False
print(1 < edad < 100)                               # True  (comparación encadenada)
print(0.1 + 0.2 == 0.3, abs(0.1 + 0.2 - 0.3) < 1e-9)  # False True  (¡floats imprecisos!)

# ---------------------------------------------------------------- CONVERSIONES
print(int("42") + 1, float("3.5") * 2, str(10) + "0", bool(""), bool("hola"))
# 43 7.0 100 False True
print(int(3.99), int("  7  "))               # 3 7  (int trunca; strip automático de espacios)

# ---------------------------------------------------------------- FORMATO DE SALIDA
precio = 1234.5
print(f"Hola {nombre}, tienes {edad} años")          # Hola Ana, tienes 25 años
print(f"Precio: ${precio:,.2f}")                     # Precio: $1,234.50
print(f"{'Izq':<10}|{'Der':>10}|{'Centro':^10}|")    # alinear columnas
print(f"{7:03d}", f"{0.256:.1%}")                    # 007 25.6%
print(f"{edad=}")                                    # edad=25  (útil para depurar)
print("a", "b", "c", sep="-", end="!\n")             # a-b-c!

# ---------------------------------------------------------------- IF / ELIF / ELSE
nota = 8.4
if nota >= 9:
    estado = "Excelente"
elif nota >= 7:
    estado = "Aprobado"
else:
    estado = "Reprobado"
print(estado)                                        # Aprobado

# Ternario
print("Mayor" if edad >= 18 else "Menor")            # Mayor

# match (Python 3.10+) — como switch
dia = 3
match dia:
    case 1 | 7:
        print("Fin de semana")
    case 2 | 3 | 4 | 5 | 6:
        print("Día laborable")                       # Día laborable
    case _:
        print("Inválido")

# ---------------------------------------------------------------- BUCLES
for i in range(3):                    # 0,1,2
    print("for", i)
for i in range(10, 0, -3):            # 10,7,4,1
    print(i, end=" ")
print()

total = 0
n = 5
while n > 0:
    total += n
    n -= 1
print("Suma 1..5 =", total)           # 15

# break, continue, else en bucles
for x in [3, 8, 11, 4]:
    if x % 2 == 0:
        continue                      # salta los pares
    if x > 10:
        print("Encontré", x)          # Encontré 11
        break
else:
    print("No se ejecuta porque hubo break")

# Tabla de multiplicar con bucles anidados
for i in range(1, 4):
    print(" ".join(f"{i * j:3d}" for j in range(1, 6)))

# ---------------------------------------------------------------- ENTRADA (descomenta para probar)
# numero = int(input("Ingrese un número: "))
# print("El doble es", numero * 2)

# Validar entrada en bucle
# while True:
#     texto = input("Edad: ")
#     if texto.isdigit():
#         edad = int(texto)
#         break
#     print("Debe ser un número entero")
