"""04 - Funciones (parámetros, *args, **kwargs, lambda, recursión, decoradores) y manejo de errores.
Ejecutar:  python 04_funciones_errores.py
"""
from functools import reduce, lru_cache


# ---------------------------------------------------------------- PARÁMETROS
def saludar(nombre, saludo="Hola", *, signo="!"):
    """Parámetro con valor por defecto y 'signo' solo por nombre (después de *)."""
    return f"{saludo}, {nombre}{signo}"

print(saludar("Ana"), saludar("Luis", "Buenas"), saludar("Eva", signo="?"))


def sumar_todo(*numeros):                 # *args → tupla
    return sum(numeros)

def crear_usuario(**datos):               # **kwargs → diccionario
    return {k: v for k, v in datos.items() if v is not None}

print(sumar_todo(1, 2, 3), sumar_todo(*[4, 5]))                # 6 9
print(crear_usuario(nombre="Ana", edad=20, email=None))        # {'nombre': 'Ana', 'edad': 20}


def estadisticas(lista):
    """Devolver varios valores (en realidad es una tupla)."""
    return min(lista), max(lista), sum(lista) / len(lista)

minimo, maximo, promedio = estadisticas([4, 8, 6])
print(minimo, maximo, promedio)                                # 4 8 6.0


# Tipado (type hints): no obliga, pero documenta y ayuda al editor
def area_rectangulo(base: float, altura: float) -> float:
    return base * altura

print(area_rectangulo(3, 4.5))


# ¡CUIDADO! Valor por defecto mutable
def agregar_mal(x, lista=[]):             # la misma lista se reutiliza entre llamadas
    lista.append(x)
    return lista

def agregar_bien(x, lista=None):
    lista = [] if lista is None else lista
    lista.append(x)
    return lista

print(agregar_mal(1), agregar_mal(2))     # [1, 2] [1, 2]  ← sorpresa
print(agregar_bien(1), agregar_bien(2))   # [1] [2]


# ---------------------------------------------------------------- LAMBDA, MAP, FILTER, REDUCE
cuadrado = lambda x: x * x
print(cuadrado(5), list(map(cuadrado, [1, 2, 3])), list(filter(lambda x: x > 1, [0, 1, 2, 3])))
print(reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1))         # 24 (producto)
print(sorted(["pera", "Uva", "kiwi"], key=str.lower), sorted(["pera", "uva", "kiwi"], key=len))


# ---------------------------------------------------------------- ÁMBITO (scope) Y CLOSURES
contador_global = 0
def incrementar():
    global contador_global
    contador_global += 1

incrementar(); incrementar()
print(contador_global)                    # 2

def crear_contador():
    cuenta = 0
    def siguiente():
        nonlocal cuenta
        cuenta += 1
        return cuenta
    return siguiente

c = crear_contador()
print(c(), c(), c())                      # 1 2 3


# ---------------------------------------------------------------- RECURSIÓN
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

@lru_cache(maxsize=None)                  # memoriza resultados → fibonacci rápido
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def aplanar(lista):
    """[1, [2, [3, 4]], 5] → [1, 2, 3, 4, 5]"""
    resultado = []
    for x in lista:
        resultado.extend(aplanar(x) if isinstance(x, list) else [x])
    return resultado

print(factorial(6), fib(50), aplanar([1, [2, [3, 4]], 5]))


# ---------------------------------------------------------------- DECORADORES
import time

def medir_tiempo(funcion):
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcion(*args, **kwargs)
        print(f"  {funcion.__name__} tardó {(time.perf_counter() - inicio) * 1000:.2f} ms")
        return resultado
    return envoltura

@medir_tiempo
def suma_lenta(n):
    return sum(range(n))

print(suma_lenta(1_000_000))


# ---------------------------------------------------------------- ERRORES / EXCEPCIONES
def dividir(a, b):
    try:
        resultado = a / b
    except ZeroDivisionError:
        print("  No se puede dividir para cero")
        return None
    except TypeError as e:
        print("  Tipos inválidos:", e)
        return None
    else:
        return resultado            # solo si no hubo error
    finally:
        print("  (finally siempre se ejecuta)")

print(dividir(10, 2), dividir(1, 0), dividir("a", 1))


# Excepción propia + raise
class SaldoInsuficienteError(Exception):
    def __init__(self, saldo, monto):
        super().__init__(f"Saldo insuficiente: tiene {saldo}, intenta retirar {monto}")
        self.saldo, self.monto = saldo, monto

def retirar(saldo, monto):
    if monto <= 0:
        raise ValueError("El monto debe ser positivo")
    if monto > saldo:
        raise SaldoInsuficienteError(saldo, monto)
    return saldo - monto

for monto in (50, -5, 500):
    try:
        print("Nuevo saldo:", retirar(100, monto))
    except (ValueError, SaldoInsuficienteError) as e:
        print("Error:", e)

# Convertir entrada de forma segura
def a_entero(texto, defecto=0):
    try:
        return int(texto)
    except (ValueError, TypeError):
        return defecto

print(a_entero("15"), a_entero("abc"), a_entero(None, -1))      # 15 0 -1

# assert: verificaciones rápidas (se usan en pruebas)
assert factorial(5) == 120, "factorial mal implementado"
print("Todas las aserciones pasaron")

# Errores comunes y su significado:
# NameError      → variable no definida (¿typo?)
# TypeError      → operación con tipos incompatibles ("a" + 1)
# ValueError     → tipo correcto pero valor inválido (int("abc"))
# IndexError     → índice fuera de rango (lista[10])
# KeyError       → clave inexistente en diccionario (usa .get)
# AttributeError → el objeto no tiene ese método (None.upper())
# IndentationError → sangría incorrecta
# ZeroDivisionError, FileNotFoundError, ModuleNotFoundError
