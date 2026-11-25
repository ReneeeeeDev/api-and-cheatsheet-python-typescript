"""Estructuras que usan los problemas 17–21: lista enlazada y árbol binario.

Las pruebas construyen las entradas con estas funciones; tu solución solo
necesita leer los atributos .valor, .siguiente, .izq y .der.
"""
from collections import deque


class Nodo:
    """Nodo de una lista enlazada simple."""

    def __init__(self, valor, siguiente=None):
        self.valor = valor
        self.siguiente = siguiente


class NodoArbol:
    """Nodo de un árbol binario."""

    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der


def crear_lista(valores):
    """[1, 2, 3] → 1 -> 2 -> 3. Devuelve la cabeza (o None si la lista está vacía)."""
    cabeza = None
    for valor in reversed(valores):
        cabeza = Nodo(valor, cabeza)
    return cabeza


def lista_a_python(cabeza, limite=10_000):
    """1 -> 2 -> 3 → [1, 2, 3]. El límite evita un bucle infinito si hay un ciclo."""
    valores = []
    while cabeza is not None and len(valores) < limite:
        valores.append(cabeza.valor)
        cabeza = cabeza.siguiente
    return valores


def crear_arbol(valores):
    """Construye un árbol desde una lista por niveles, como en LeetCode.

    [3, 9, 20, None, None, 15, 7] →      3
                                        / \\
                                       9   20
                                          /  \\
                                         15   7
    """
    if not valores or valores[0] is None:
        return None
    raiz = NodoArbol(valores[0])
    cola = deque([raiz])
    i = 1
    while cola and i < len(valores):
        actual = cola.popleft()
        if i < len(valores) and valores[i] is not None:
            actual.izq = NodoArbol(valores[i])
            cola.append(actual.izq)
        i += 1
        if i < len(valores) and valores[i] is not None:
            actual.der = NodoArbol(valores[i])
            cola.append(actual.der)
        i += 1
    return raiz
