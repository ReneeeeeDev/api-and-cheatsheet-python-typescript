// Soluciones de referencia de los 30 problemas de entrevista (PROBLEMAS.md), en JavaScript.
// Mismas ideas que soluciones.py. Comprobarlas: node pruebas.js
// Intenta cada problema en mis_soluciones.js ANTES de leer esto.

// ======================================================== A. ARREGLOS Y HASH
// 1. Set de vistos. O(n).
function contieneDuplicado(nums) {
  const vistos = new Set();
  for (const n of nums) {
    if (vistos.has(n)) return true;
    vistos.add(n);
  }
  return false;
}

// 2. Boyer-Moore: el mayoritario sobrevive a las cancelaciones. O(n), O(1) espacio.
function elementoMayoritario(nums) {
  let candidato = null;
  let votos = 0;
  for (const n of nums) {
    if (votos === 0) candidato = n;
    votos += n === candidato ? 1 : -1;
  }
  return candidato;
}

// 3. Set + contar solo desde el inicio de cada secuencia. O(n).
function secuenciaConsecutivaMasLarga(nums) {
  const conjunto = new Set(nums);
  let mejor = 0;
  for (const n of conjunto) {
    if (!conjunto.has(n - 1)) {
      let largo = 1;
      while (conjunto.has(n + largo)) largo++;
      mejor = Math.max(mejor, largo);
    }
  }
  return mejor;
}

// 4. Sumas prefijas + Map: si (prefijo - k) ya apareció, hay un subarreglo que suma k. O(n).
function subarreglosSumaK(nums, k) {
  const conteo = new Map([[0, 1]]);
  let prefijo = 0;
  let total = 0;
  for (const n of nums) {
    prefijo += n;
    total += conteo.get(prefijo - k) ?? 0;
    conteo.set(prefijo, (conteo.get(prefijo) ?? 0) + 1);
  }
  return total;
}

// 5. Producto a la izquierda × producto a la derecha, sin división. O(n).
function productoExceptoSiMismo(nums) {
  const resultado = new Array(nums.length).fill(1);
  let izquierda = 1;
  for (let i = 0; i < nums.length; i++) {
    resultado[i] = izquierda;
    izquierda *= nums[i];
  }
  let derecha = 1;
  for (let i = nums.length - 1; i >= 0; i--) {
    resultado[i] *= derecha;
    derecha *= nums[i];
  }
  return resultado;
}

// ============================================================ B. DOS PUNTEROS
// 6. Puntero de escritura y de lectura en el mismo arreglo. O(n), O(1) espacio.
function moverCeros(nums) {
  let escribir = 0;
  for (let leer = 0; leer < nums.length; leer++) {
    if (nums[leer] !== 0) {
      [nums[escribir], nums[leer]] = [nums[leer], nums[escribir]];
      escribir++;
    }
  }
  return nums;
}

// 7. Un puntero por arreglo; siempre se toma el menor. O(n + m).
function fusionarOrdenadas(a, b) {
  let i = 0;
  let j = 0;
  const resultado = [];
  while (i < a.length && j < b.length) {
    if (a[i] <= b[j]) resultado.push(a[i++]);
    else resultado.push(b[j++]);
  }
  return resultado.concat(a.slice(i), b.slice(j));
}

// 8. Ordenar + fijar uno + dos punteros. O(n²).
// ¡Ojo! sort() sin comparador ordena como texto: [10, 9, 1].sort() → [1, 10, 9].
function tresSuma(nums) {
  nums = [...nums].sort((x, y) => x - y);
  const resultado = [];
  for (let i = 0; i < nums.length - 2; i++) {
    if (i > 0 && nums[i] === nums[i - 1]) continue;
    let izq = i + 1;
    let der = nums.length - 1;
    while (izq < der) {
      const suma = nums[i] + nums[izq] + nums[der];
      if (suma < 0) izq++;
      else if (suma > 0) der--;
      else {
        resultado.push([nums[i], nums[izq], nums[der]]);
        izq++;
        der--;
        while (izq < der && nums[izq] === nums[izq - 1]) izq++;
      }
    }
  }
  return resultado;
}

// 9. Punteros en los extremos; mover el lado más bajo. O(n).
function contenedorMasAgua(alturas) {
  let izq = 0;
  let der = alturas.length - 1;
  let mejor = 0;
  while (izq < der) {
    mejor = Math.max(mejor, (der - izq) * Math.min(alturas[izq], alturas[der]));
    if (alturas[izq] < alturas[der]) izq++;
    else der--;
  }
  return mejor;
}

// ======================================================= C. VENTANA DESLIZANTE
// 10. Ventana fija: sumar el que entra y restar el que sale. O(n).
function maxSumaVentana(nums, k) {
  if (k <= 0 || k > nums.length) return null;
  let ventana = 0;
  for (let i = 0; i < k; i++) ventana += nums[i];
  let mejor = ventana;
  for (let i = k; i < nums.length; i++) {
    ventana += nums[i] - nums[i - k];
    mejor = Math.max(mejor, ventana);
  }
  return mejor;
}

// 11. Ventana variable con la última posición de cada letra. O(n).
function subcadenaSinRepetir(s) {
  const ultima = new Map();
  let inicio = 0;
  let mejor = 0;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (ultima.has(c) && ultima.get(c) >= inicio) inicio = ultima.get(c) + 1;
    ultima.set(c, i);
    mejor = Math.max(mejor, i - inicio + 1);
  }
  return mejor;
}

// =================================================================== D. PILAS
// 12. Pila: un operador saca dos valores y apila el resultado. O(n).
function evaluarRpn(tokens) {
  const pila = [];
  const operaciones = {
    "+": (a, b) => a + b,
    "-": (a, b) => a - b,
    "*": (a, b) => a * b,
    "/": (a, b) => Math.trunc(a / b), // trunca hacia 0
  };
  for (const t of tokens) {
    if (t in operaciones) {
      const b = pila.pop(); // ¡el orden importa!: b sale primero
      const a = pila.pop();
      pila.push(operaciones[t](a, b));
    } else {
      pila.push(Number(t));
    }
  }
  return pila[0];
}

// 13. Pila monótona de índices que esperan un día más cálido. O(n).
function temperaturasDiarias(temps) {
  const respuesta = new Array(temps.length).fill(0);
  const pila = [];
  temps.forEach((t, i) => {
    while (pila.length && temps[pila[pila.length - 1]] < t) {
      const j = pila.pop();
      respuesta[j] = i - j;
    }
    pila.push(i);
  });
  return respuesta;
}

// 14. Cada elemento guarda también el mínimo hasta ese punto: todo O(1).
class PilaMinima {
  constructor() {
    this.datos = []; // pares [valor, mínimo hasta aquí]
  }
  apilar(x) {
    const minimo = this.datos.length ? Math.min(x, this.minimo()) : x;
    this.datos.push([x, minimo]);
  }
  desapilar() {
    return this.datos.pop()[0];
  }
  tope() {
    return this.datos[this.datos.length - 1][0];
  }
  minimo() {
    return this.datos[this.datos.length - 1][1];
  }
}

// ======================================================== E. BÚSQUEDA BINARIA
// 15. Búsqueda binaria sobre la respuesta: el mayor r con r*r <= n. O(log n).
function raizEntera(n) {
  let izq = 0;
  let der = n;
  while (izq <= der) {
    const medio = Math.floor((izq + der) / 2);
    if (medio * medio <= n) izq = medio + 1;
    else der = medio - 1;
  }
  return der;
}

// 16. En cada paso al menos una mitad está ordenada. O(log n).
function buscarEnRotado(nums, objetivo) {
  let izq = 0;
  let der = nums.length - 1;
  while (izq <= der) {
    const medio = Math.floor((izq + der) / 2);
    if (nums[medio] === objetivo) return medio;
    if (nums[izq] <= nums[medio]) {
      if (nums[izq] <= objetivo && objetivo < nums[medio]) der = medio - 1;
      else izq = medio + 1;
    } else {
      if (nums[medio] < objetivo && objetivo <= nums[der]) izq = medio + 1;
      else der = medio - 1;
    }
  }
  return -1;
}

// ======================================================= F. LISTAS ENLAZADAS
// 17. Tres punteros: anterior, actual, siguiente. O(n), O(1) espacio.
function invertirLista(cabeza) {
  let anterior = null;
  let actual = cabeza;
  while (actual !== null) {
    const siguiente = actual.siguiente;
    actual.siguiente = anterior;
    anterior = actual;
    actual = siguiente;
  }
  return anterior;
}

// 18. Floyd (tortuga y liebre). O(n), O(1) espacio.
function tieneCiclo(cabeza) {
  let lento = cabeza;
  let rapido = cabeza;
  while (rapido !== null && rapido.siguiente !== null) {
    lento = lento.siguiente;
    rapido = rapido.siguiente.siguiente;
    if (lento === rapido) return true;
  }
  return false;
}

// ================================================================= G. ÁRBOLES
// 19. DFS recursivo: 1 + la altura del subárbol más alto. O(n).
function alturaArbol(raiz) {
  if (raiz === null) return 0;
  return 1 + Math.max(alturaArbol(raiz.izq), alturaArbol(raiz.der));
}

// 20. BFS por niveles. O(n).
// Nota: shift() es O(n); en colas muy grandes usa un índice de lectura en su lugar.
function recorridoPorNiveles(raiz) {
  if (raiz === null) return [];
  const niveles = [];
  const cola = [raiz];
  while (cola.length) {
    const nivel = [];
    for (let k = cola.length; k > 0; k--) {
      const nodo = cola.shift();
      nivel.push(nodo.valor);
      if (nodo.izq) cola.push(nodo.izq);
      if (nodo.der) cola.push(nodo.der);
    }
    niveles.push(nivel);
  }
  return niveles;
}

// 21. Cada nodo debe estar en el rango (minimo, maximo) heredado de sus ancestros. O(n).
function esBstValido(raiz, minimo = -Infinity, maximo = Infinity) {
  if (raiz === null) return true;
  if (raiz.valor <= minimo || raiz.valor >= maximo) return false;
  return esBstValido(raiz.izq, minimo, raiz.valor) && esBstValido(raiz.der, raiz.valor, maximo);
}

// ================================================================== H. GRAFOS
// 22. Cada "1" sin visitar inicia un BFS que marca toda su isla. O(filas × columnas).
function contarIslas(mapa) {
  if (!mapa.length) return 0;
  const filas = mapa.length;
  const columnas = mapa[0].length;
  const visitados = new Set();
  const clave = (f, c) => `${f},${c}`;
  let islas = 0;
  for (let f = 0; f < filas; f++) {
    for (let c = 0; c < columnas; c++) {
      if (mapa[f][c] !== "1" || visitados.has(clave(f, c))) continue;
      islas++;
      visitados.add(clave(f, c));
      const cola = [[f, c]];
      for (let lectura = 0; lectura < cola.length; lectura++) {
        const [x, y] = cola[lectura];
        for (const [nx, ny] of [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]) {
          if (nx >= 0 && nx < filas && ny >= 0 && ny < columnas &&
              mapa[nx][ny] === "1" && !visitados.has(clave(nx, ny))) {
            visitados.add(clave(nx, ny));
            cola.push([nx, ny]);
          }
        }
      }
    }
  }
  return islas;
}

// 23. Orden topológico (Kahn). Si no se pueden tomar todas, hay un ciclo → []. O(V + E).
function ordenCursos(n, prerrequisitos) {
  const siguientes = Array.from({ length: n }, () => []);
  const pendientes = new Array(n).fill(0);
  for (const [materia, requisito] of prerrequisitos) {
    siguientes[requisito].push(materia);
    pendientes[materia]++;
  }
  const cola = [];
  for (let i = 0; i < n; i++) if (pendientes[i] === 0) cola.push(i);
  const orden = [];
  for (let lectura = 0; lectura < cola.length; lectura++) {
    const actual = cola[lectura];
    orden.push(actual);
    for (const materia of siguientes[actual]) {
      if (--pendientes[materia] === 0) cola.push(materia);
    }
  }
  return orden.length === n ? orden : [];
}

// ============================================================ I. BACKTRACKING
// 24. Para cada elemento: lo tomo / no lo tomo. O(n · 2ⁿ).
function subconjuntos(nums) {
  const resultado = [];
  const actual = [];
  const explorar = (i) => {
    if (i === nums.length) {
      resultado.push([...actual]);
      return;
    }
    actual.push(nums[i]);
    explorar(i + 1);
    actual.pop();
    explorar(i + 1);
  };
  explorar(0);
  return resultado;
}

// 25. Elegir uno de los que quedan, recursión, deshacer. O(n · n!).
function permutaciones(nums) {
  const resultado = [];
  const actual = [];
  const usados = new Array(nums.length).fill(false);
  const explorar = () => {
    if (actual.length === nums.length) {
      resultado.push([...actual]);
      return;
    }
    nums.forEach((n, i) => {
      if (usados[i]) return;
      usados[i] = true;
      actual.push(n);
      explorar();
      actual.pop();
      usados[i] = false;
    });
  };
  explorar();
  return resultado;
}

// ================================================ J. PROGRAMACIÓN DINÁMICA
// 26. formas(n) = formas(n-1) + formas(n-2). O(n), O(1) espacio.
function formasSubirEscalera(n) {
  let anterior = 1;
  let actual = 1;
  for (let i = 1; i < n; i++) [anterior, actual] = [actual, anterior + actual];
  return actual;
}

// 27. Kadane: ¿sigo la racha o empiezo de nuevo aquí? O(n).
function maxSubarreglo(nums) {
  let mejor = nums[0];
  let actual = nums[0];
  for (let i = 1; i < nums.length; i++) {
    actual = Math.max(nums[i], actual + nums[i]);
    mejor = Math.max(mejor, actual);
  }
  return mejor;
}

// 28. Tabla dp[i][j] = LCS de a[:i] y b[:j]. O(len(a) × len(b)).
function subsecuenciaComunMasLarga(a, b) {
  const dp = Array.from({ length: a.length + 1 }, () => new Array(b.length + 1).fill(0));
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1] + 1
        : Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  return dp[a.length][b.length];
}

// ================================================ K. ORDENAMIENTO Y DISEÑO
// 29. Divide y vencerás + fusionar (problema 7). O(n log n), estable, no modifica la entrada.
function mergeSort(lista) {
  if (lista.length <= 1) return [...lista];
  const medio = Math.floor(lista.length / 2);
  return fusionarOrdenadas(mergeSort(lista.slice(0, medio)), mergeSort(lista.slice(medio)));
}

// 30. Map recuerda el orden de inserción: borrar y volver a insertar mueve la clave al final;
// la primera clave es la usada hace más tiempo. obtener y poner en O(1).
class CacheLRU {
  constructor(capacidad) {
    this.capacidad = capacidad;
    this.datos = new Map();
  }
  obtener(clave) {
    if (!this.datos.has(clave)) return -1;
    const valor = this.datos.get(clave);
    this.datos.delete(clave);
    this.datos.set(clave, valor);
    return valor;
  }
  poner(clave, valor) {
    this.datos.delete(clave);
    this.datos.set(clave, valor);
    if (this.datos.size > this.capacidad) this.datos.delete(this.datos.keys().next().value);
  }
}

module.exports = {
  contieneDuplicado, elementoMayoritario, secuenciaConsecutivaMasLarga, subarreglosSumaK,
  productoExceptoSiMismo, moverCeros, fusionarOrdenadas, tresSuma, contenedorMasAgua,
  maxSumaVentana, subcadenaSinRepetir, evaluarRpn, temperaturasDiarias, PilaMinima,
  raizEntera, buscarEnRotado, invertirLista, tieneCiclo, alturaArbol, recorridoPorNiveles,
  esBstValido, contarIslas, ordenCursos, subconjuntos, permutaciones, formasSubirEscalera,
  maxSubarreglo, subsecuenciaComunMasLarga, mergeSort, CacheLRU,
};
