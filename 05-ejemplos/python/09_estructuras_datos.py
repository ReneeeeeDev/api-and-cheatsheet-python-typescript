"""09 - Estructuras de datos y algoritmos clásicos: pila, cola, lista enlazada, búsqueda y ordenamiento.
Ejecutar:  python 09_estructuras_datos.py
"""
from collections import deque
import heapq


# ---------------------------------------------------------------- PILA (LIFO)
pila = []
pila.append("a"); pila.append("b"); pila.append("c")
print("pila:", pila, "saco:", pila.pop(), "tope:", pila[-1])      # saco c, tope b

def deshacer_demo():
    historial = []
    texto = ""
    for accion in ["Hola", " mundo", "!"]:
        historial.append(texto)
        texto += accion
    print("texto:", texto)
    texto = historial.pop()                                        # Ctrl+Z
    print("después de deshacer:", texto)
deshacer_demo()

# ---------------------------------------------------------------- COLA (FIFO)
cola = deque()
cola.append("cliente1"); cola.append("cliente2"); cola.append("cliente3")
print("atiendo a:", cola.popleft(), "| quedan:", list(cola))

# Cola de prioridad (el menor número sale primero)
tickets = []
heapq.heappush(tickets, (2, "Impresora sin tinta"))
heapq.heappush(tickets, (1, "Servidor caído"))
heapq.heappush(tickets, (3, "Cambiar fondo de pantalla"))
while tickets:
    prioridad, desc = heapq.heappop(tickets)
    print(f"  prioridad {prioridad}: {desc}")


# ---------------------------------------------------------------- LISTA ENLAZADA
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def agregar(self, valor):                  # al final: O(n)
        nuevo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    def eliminar(self, valor):
        anterior, actual = None, self.cabeza
        while actual:
            if actual.valor == valor:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                self.tamanio -= 1
                return True
            anterior, actual = actual, actual.siguiente
        return False

    def invertir(self):
        anterior, actual = None, self.cabeza
        while actual:
            actual.siguiente, anterior, actual = anterior, actual, actual.siguiente
        self.cabeza = anterior

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.valor
            actual = actual.siguiente

    def __str__(self):
        return " -> ".join(map(str, self)) + " -> None"

le = ListaEnlazada()
for v in [1, 2, 3, 4]:
    le.agregar(v)
le.eliminar(3)
print(le, "| tamaño:", le.tamanio)
le.invertir()
print("invertida:", le)


# ---------------------------------------------------------------- BÚSQUEDA
def busqueda_lineal(lista, x):                 # O(n)
    for i, v in enumerate(lista):
        if v == x:
            return i
    return -1

def busqueda_binaria(lista, x):                # O(log n), lista ORDENADA
    izq, der = 0, len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == x:
            return medio
        izq, der = (medio + 1, der) if lista[medio] < x else (izq, medio - 1)
    return -1

datos = list(range(0, 100, 3))
print("lineal:", busqueda_lineal(datos, 42), "binaria:", busqueda_binaria(datos, 42), busqueda_binaria(datos, 43))


# ---------------------------------------------------------------- ORDENAMIENTO
def burbuja(a):                                # O(n²)
    a = a[:]
    for i in range(len(a) - 1):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def seleccion(a):                              # O(n²): busca el mínimo y lo pone al inicio
    a = a[:]
    for i in range(len(a)):
        m = min(range(i, len(a)), key=a.__getitem__)
        a[i], a[m] = a[m], a[i]
    return a

def insercion(a):                              # O(n²), rápido si casi ordenado
    a = a[:]
    for i in range(1, len(a)):
        actual, j = a[i], i - 1
        while j >= 0 and a[j] > actual:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a

def merge_sort(a):                             # O(n log n): divide y vencerás
    if len(a) <= 1:
        return a
    medio = len(a) // 2
    izq, der = merge_sort(a[:medio]), merge_sort(a[medio:])
    resultado, i, j = [], 0, 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    return resultado + izq[i:] + der[j:]

def quick_sort(a):                             # O(n log n) promedio
    if len(a) <= 1:
        return a
    pivote = a[len(a) // 2]
    return (quick_sort([x for x in a if x < pivote]) + [x for x in a if x == pivote]
            + quick_sort([x for x in a if x > pivote]))

desordenada = [29, 3, 72, 15, 3, 88, 41]
for f in (burbuja, seleccion, insercion, merge_sort, quick_sort):
    print(f"{f.__name__:<11}", f(desordenada))

# Complejidad (Big O), de mejor a peor:
# O(1) acceso por índice / dict   O(log n) búsqueda binaria   O(n) recorrer
# O(n log n) merge/quick/sorted   O(n²) doble bucle           O(2^n) fibonacci recursivo sin memo
