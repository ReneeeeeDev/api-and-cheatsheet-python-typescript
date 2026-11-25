// Estructuras que usan los problemas 17–21: lista enlazada y árbol binario.
// Las pruebas construyen las entradas con estas funciones; tu solución solo
// necesita leer .valor, .siguiente, .izq y .der.

class Nodo {
  constructor(valor, siguiente = null) {
    this.valor = valor;
    this.siguiente = siguiente;
  }
}

class NodoArbol {
  constructor(valor, izq = null, der = null) {
    this.valor = valor;
    this.izq = izq;
    this.der = der;
  }
}

// [1, 2, 3] → 1 -> 2 -> 3. Devuelve la cabeza (o null si está vacía).
function crearLista(valores) {
  let cabeza = null;
  for (let i = valores.length - 1; i >= 0; i--) cabeza = new Nodo(valores[i], cabeza);
  return cabeza;
}

// 1 -> 2 -> 3 → [1, 2, 3]. El límite evita un bucle infinito si hay un ciclo.
function listaAArray(cabeza, limite = 10000) {
  const valores = [];
  while (cabeza !== null && valores.length < limite) {
    valores.push(cabeza.valor);
    cabeza = cabeza.siguiente;
  }
  return valores;
}

// Árbol desde una lista por niveles, como en LeetCode: [3, 9, 20, null, null, 15, 7]
function crearArbol(valores) {
  if (!valores.length || valores[0] === null) return null;
  const raiz = new NodoArbol(valores[0]);
  const cola = [raiz];
  let i = 1;
  while (cola.length && i < valores.length) {
    const actual = cola.shift();
    if (i < valores.length && valores[i] !== null) {
      actual.izq = new NodoArbol(valores[i]);
      cola.push(actual.izq);
    }
    i++;
    if (i < valores.length && valores[i] !== null) {
      actual.der = new NodoArbol(valores[i]);
      cola.push(actual.der);
    }
    i++;
  }
  return raiz;
}

module.exports = { Nodo, NodoArbol, crearLista, listaAArray, crearArbol };
