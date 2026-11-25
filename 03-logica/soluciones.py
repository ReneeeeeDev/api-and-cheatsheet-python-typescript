"""Soluciones de los 30 ejercicios. Ejecutar: python soluciones.py (corre las pruebas)."""
import math
import re
import unicodedata
from collections import Counter, defaultdict


# ----------------------------------------------------------------- NIVEL 1
def es_par(n):
    return n % 2 == 0


def mayor_de_tres(a, b, c):
    mayor = a
    if b > mayor:
        mayor = b
    if c > mayor:
        mayor = c
    return mayor


def factorial(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def factorial_rec(n):
    return 1 if n <= 1 else n * factorial_rec(n - 1)


def suma_digitos(n):
    n, total = abs(n), 0
    while n > 0:
        total += n % 10       # último dígito
        n //= 10              # quitar último dígito
    return total


def invertir_texto(s):
    resultado = ""
    for letra in s:
        resultado = letra + resultado
    return resultado


def quitar_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def contar_vocales(s):
    return sum(1 for c in quitar_tildes(s.lower()) if c in "aeiou")


def tabla_multiplicar(n):
    return [n * i for i in range(1, 11)]


def celsius_a_fahrenheit(c):
    return c * 9 / 5 + 32


def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0


def fizzbuzz(n):
    salida = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            salida.append("FizzBuzz")
        elif i % 3 == 0:
            salida.append("Fizz")
        elif i % 5 == 0:
            salida.append("Buzz")
        else:
            salida.append(i)
    return salida


# ----------------------------------------------------------------- NIVEL 2
def es_primo(n):
    if n < 2:
        return False
    for d in range(2, int(math.sqrt(n)) + 1):
        if n % d == 0:
            return False
    return True


def fibonacci(n):
    serie, a, b = [], 0, 1
    for _ in range(n):
        serie.append(a)
        a, b = b, a + b
    return serie


def es_palindromo(s):
    limpio = [c for c in quitar_tildes(s.lower()) if c.isalnum()]
    return limpio == limpio[::-1]


def contar_palabras(texto):
    palabras = re.findall(r"\w+", texto.lower())
    return dict(Counter(palabras))


def segundo_mayor(lista):
    unicos = sorted(set(lista), reverse=True)
    return unicos[1] if len(unicos) >= 2 else None


def eliminar_duplicados(lista):
    vistos, resultado = set(), []
    for x in lista:
        if x not in vistos:
            vistos.add(x)
            resultado.append(x)
    return resultado


def son_anagramas(a, b):
    normal = lambda s: sorted(quitar_tildes(s.lower().replace(" ", "")))
    return normal(a) == normal(b)


def mcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mcm(a, b):
    return a * b // mcd(a, b)


def decimal_a_binario(n):
    if n == 0:
        return "0"
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n //= 2
    return bits


def validar_cedula(cedula):
    if not (len(cedula) == 10 and cedula.isdigit()):
        return False
    provincia = int(cedula[:2])
    if not (1 <= provincia <= 24 or provincia == 30) or int(cedula[2]) >= 6:
        return False
    suma = 0
    for i, coef in enumerate([2, 1, 2, 1, 2, 1, 2, 1, 2]):
        p = int(cedula[i]) * coef
        suma += p - 9 if p > 9 else p
    return (10 - suma % 10) % 10 == int(cedula[9])


# ----------------------------------------------------------------- NIVEL 3
def busqueda_binaria(lista, x):
    izq, der = 0, len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == x:
            return medio
        if lista[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1


def ordenar_burbuja(lista):
    a = lista[:]                          # no modificar la original
    n = len(a)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):        # los últimos i ya están en su lugar
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                hubo_cambio = True
        if not hubo_cambio:               # optimización: ya está ordenada
            break
    return a


def parentesis_balanceados(s):
    pares = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in s:
        if c in "([{":
            pila.append(c)
        elif c in pares:
            if not pila or pila.pop() != pares[c]:
                return False
    return not pila


def comprimir(s):
    if not s:
        return ""
    resultado, actual, cuenta = [], s[0], 1
    for c in s[1:]:
        if c == actual:
            cuenta += 1
        else:
            resultado.append(f"{actual}{cuenta}")
            actual, cuenta = c, 1
    resultado.append(f"{actual}{cuenta}")
    return "".join(resultado)


def rotar_matriz(m):
    n = len(m)
    return [[m[n - 1 - f][c] for f in range(n)] for c in range(n)]


def dos_suma(nums, objetivo):
    vistos = {}                            # valor -> índice
    for i, x in enumerate(nums):
        falta = objetivo - x
        if falta in vistos:
            return [vistos[falta], i]
        vistos[x] = i
    return None


def numero_romano(n):
    valores = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
               (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    resultado = ""
    for valor, simbolo in valores:
        while n >= valor:
            resultado += simbolo
            n -= valor
    return resultado


def agrupar_por(registros, clave):
    grupos = defaultdict(list)
    for r in registros:
        grupos[r[clave]].append(r)
    return dict(grupos)


def calcular_nomina(empleados, tasa_iess=0.0945):
    detalle = []
    for e in empleados:
        aporte = round(e["sueldo"] * tasa_iess, 2)
        detalle.append({"nombre": e["nombre"], "aporte": aporte, "neto": round(e["sueldo"] - aporte, 2)})
    total = round(sum(d["neto"] for d in detalle), 2)
    return detalle, total


def cajero(monto, denominaciones=(20, 10, 5, 1)):
    resultado = {}
    for d in denominaciones:
        cantidad, monto = divmod(monto, d)
        if cantidad:
            resultado[d] = cantidad
    return resultado


# ----------------------------------------------------------------- PRUEBAS
if __name__ == "__main__":
    casos = [
        (es_par(4) and not es_par(7), "es_par"),
        (mayor_de_tres(3, 9, 5) == 9, "mayor_de_tres"),
        (factorial(5) == 120 and factorial_rec(5) == 120 and factorial(0) == 1, "factorial"),
        (suma_digitos(1234) == 10, "suma_digitos"),
        (invertir_texto("hola") == "aloh", "invertir_texto"),
        (contar_vocales("Murciélago") == 5, "contar_vocales"),
        (tabla_multiplicar(3)[-1] == 30, "tabla_multiplicar"),
        (celsius_a_fahrenheit(100) == 212, "celsius_a_fahrenheit"),
        (es_bisiesto(2024) and not es_bisiesto(1900) and es_bisiesto(2000), "es_bisiesto"),
        (fizzbuzz(15)[-1] == "FizzBuzz" and fizzbuzz(5)[2] == "Fizz", "fizzbuzz"),
        ([n for n in range(20) if es_primo(n)] == [2, 3, 5, 7, 11, 13, 17, 19], "es_primo"),
        (fibonacci(7) == [0, 1, 1, 2, 3, 5, 8], "fibonacci"),
        (es_palindromo("Anita lava la tina") and not es_palindromo("hola"), "es_palindromo"),
        (contar_palabras("Hola, hola mundo!") == {"hola": 2, "mundo": 1}, "contar_palabras"),
        (segundo_mayor([4, 9, 9, 2]) == 4 and segundo_mayor([1, 1]) is None, "segundo_mayor"),
        (eliminar_duplicados([3, 1, 3, 2, 1]) == [3, 1, 2], "eliminar_duplicados"),
        (son_anagramas("Roma", "amor") and not son_anagramas("abc", "abd"), "son_anagramas"),
        (mcd(48, 18) == 6 and mcm(4, 6) == 12, "mcd/mcm"),
        (decimal_a_binario(10) == "1010" and decimal_a_binario(0) == "0", "decimal_a_binario"),
        (validar_cedula("1710034065") and not validar_cedula("1710034064"), "validar_cedula"),
        (busqueda_binaria([1, 3, 5, 7, 9], 7) == 3 and busqueda_binaria([1, 3], 4) == -1, "busqueda_binaria"),
        (ordenar_burbuja([5, 2, 9, 1]) == [1, 2, 5, 9], "ordenar_burbuja"),
        (parentesis_balanceados("({[]})") and not parentesis_balanceados("([)]"), "parentesis"),
        (comprimir("aaabbc") == "a3b2c1", "comprimir"),
        (rotar_matriz([[1, 2], [3, 4]]) == [[3, 1], [4, 2]], "rotar_matriz"),
        (dos_suma([2, 7, 11, 15], 9) == [0, 1], "dos_suma"),
        (numero_romano(1994) == "MCMXCIV", "numero_romano"),
        (len(agrupar_por([{"c": "A"}, {"c": "B"}, {"c": "A"}], "c")["A"]) == 2, "agrupar_por"),
        (calcular_nomina([{"nombre": "Ana", "sueldo": 1000}])[1] == 905.5, "calcular_nomina"),
        (cajero(38) == {20: 1, 10: 1, 5: 1, 1: 3}, "cajero"),
    ]
    fallos = [nombre for ok, nombre in casos if not ok]
    for ok, nombre in casos:
        print(("OK    " if ok else "FALLO ") + nombre)
    print(f"\n{len(casos) - len(fallos)}/{len(casos)} correctas")
