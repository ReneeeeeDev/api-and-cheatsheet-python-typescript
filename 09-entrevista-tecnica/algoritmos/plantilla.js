// Plantilla para practicar los 30 problemas de PROBLEMAS.md en JavaScript.
//
// 1. Copia este archivo:  copy plantilla.js mis_soluciones.js     (Linux/Mac: cp)
// 2. Resuelve un problema reemplazando `pendiente()`.
// 3. Prueba:              node pruebas.js mis_soluciones.js 1     (o sin número para todos)
//
// Cronométrate: ⭐ 10 min · ⭐⭐ 20 min · ⭐⭐⭐ 30 min. Di en voz alta lo que piensas.
// Listas enlazadas y árboles usan las clases de estructuras.js (.valor, .siguiente, .izq, .der).

const pendiente = () => {
  throw new Error("pendiente");
};

// ======================================================== A. ARREGLOS Y HASH
// 1. ¿Algún valor aparece dos veces? [1, 2, 3, 1] → true
function contieneDuplicado(nums) { pendiente(); }

// 2. El valor que aparece más de n/2 veces. [2, 2, 1, 1, 1, 2, 2] → 2
function elementoMayoritario(nums) { pendiente(); }

// 3. Largo de la mayor secuencia de enteros consecutivos, en O(n). [100, 4, 200, 1, 3, 2] → 4
function secuenciaConsecutivaMasLarga(nums) { pendiente(); }

// 4. Cuántos subarreglos contiguos suman k (puede haber negativos). [1, 1, 1], 2 → 2
function subarreglosSumaK(nums, k) { pendiente(); }

// 5. resultado[i] = producto de todos menos nums[i], SIN división. [1, 2, 3, 4] → [24, 12, 8, 6]
function productoExceptoSiMismo(nums) { pendiente(); }

// ============================================================ B. DOS PUNTEROS
// 6. Mover los ceros al final EN EL MISMO arreglo. [0, 1, 0, 3, 12] → [1, 3, 12, 0, 0]
function moverCeros(nums) { pendiente(); }

// 7. Unir dos arreglos ordenados sin sort(). [1, 3, 5], [2, 4] → [1, 2, 3, 4, 5]
function fusionarOrdenadas(a, b) { pendiente(); }

// 8. Todas las tripletas distintas que suman 0. [-1, 0, 1, 2, -1, -4] → [[-1, -1, 2], [-1, 0, 1]]
function tresSuma(nums) { pendiente(); }

// 9. Área máxima entre dos líneas: (j - i) * min(h[i], h[j]). [1, 8, 6, 2, 5, 4, 8, 3, 7] → 49
function contenedorMasAgua(alturas) { pendiente(); }

// ======================================================= C. VENTANA DESLIZANTE
// 10. Mayor suma de k elementos seguidos; null si k no es válido. [2, 1, 5, 1, 3, 2], 3 → 9
function maxSumaVentana(nums, k) { pendiente(); }

// 11. Largo de la subcadena más larga sin letras repetidas. "abcabcbb" → 3
function subcadenaSinRepetir(s) { pendiente(); }

// =================================================================== D. PILAS
// 12. Evaluar notación polaca inversa; la división trunca hacia 0. ["2", "1", "+", "3", "*"] → 9
function evaluarRpn(tokens) { pendiente(); }

// 13. Días a esperar hasta uno más cálido. [73, 74, 75, 71, 69, 72, 76, 73] → [1, 1, 4, 2, 1, 1, 0, 0]
function temperaturasDiarias(temps) { pendiente(); }

// 14. Pila con apilar, desapilar, tope y minimo, todas en O(1).
class PilaMinima {
  constructor() { pendiente(); }
  apilar(x) { pendiente(); }
  desapilar() { pendiente(); }
  tope() { pendiente(); }
  minimo() { pendiente(); }
}

// ======================================================== E. BÚSQUEDA BINARIA
// 15. Parte entera de √n sin Math.sqrt ni ** 0.5. 8 → 2
function raizEntera(n) { pendiente(); }

// 16. Índice en un arreglo ordenado y rotado, en O(log n). [4, 5, 6, 7, 0, 1, 2], 0 → 4
function buscarEnRotado(nums, objetivo) { pendiente(); }

// ======================================================= F. LISTAS ENLAZADAS
// 17. Invertir la lista enlazada y devolver la nueva cabeza. 1->2->3 → 3->2->1
function invertirLista(cabeza) { pendiente(); }

// 18. ¿La lista enlazada tiene un ciclo? Con O(1) de memoria extra.
function tieneCiclo(cabeza) { pendiente(); }

// ================================================================= G. ÁRBOLES
// 19. Número de niveles del árbol (null → 0).
function alturaArbol(raiz) { pendiente(); }

// 20. Valores agrupados por nivel. [3, 9, 20, null, null, 15, 7] → [[3], [9, 20], [15, 7]]
function recorridoPorNiveles(raiz) { pendiente(); }

// 21. ¿Es un árbol binario de búsqueda (izq < nodo < der en TODO el subárbol)?
function esBstValido(raiz) { pendiente(); }

// ================================================================== H. GRAFOS
// 22. Grupos de "1" conectados en horizontal/vertical. ["110", "010", "001"] → 2
function contarIslas(mapa) { pendiente(); }

// 23. Orden para tomar las materias 0..n-1; pares [materia, requisito]. [] si hay ciclo.
function ordenCursos(n, prerrequisitos) { pendiente(); }

// ============================================================ I. BACKTRACKING
// 24. Todos los subconjuntos. [1, 2] → [[], [1], [2], [1, 2]] (en cualquier orden)
function subconjuntos(nums) { pendiente(); }

// 25. Todas las permutaciones (valores distintos). [1, 2] → [[1, 2], [2, 1]]
function permutaciones(nums) { pendiente(); }

// ================================================ J. PROGRAMACIÓN DINÁMICA
// 26. Formas de subir n escalones de 1 en 1 o de 2 en 2. 5 → 8
function formasSubirEscalera(n) { pendiente(); }

// 27. Mayor suma de un subarreglo contiguo. [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6
function maxSubarreglo(nums) { pendiente(); }

// 28. Largo de la subsecuencia común más larga. "abcde", "ace" → 3
function subsecuenciaComunMasLarga(a, b) { pendiente(); }

// ================================================ K. ORDENAMIENTO Y DISEÑO
// 29. Ordenar con merge sort, sin modificar el arreglo original.
function mergeSort(lista) { pendiente(); }

// 30. Caché con capacidad fija que expulsa la clave usada hace más tiempo.
//     obtener(clave) → valor o -1; poner(clave, valor). Ambas en O(1).
class CacheLRU {
  constructor(capacidad) { pendiente(); }
  obtener(clave) { pendiente(); }
  poner(clave, valor) { pendiente(); }
}

module.exports = {
  contieneDuplicado, elementoMayoritario, secuenciaConsecutivaMasLarga, subarreglosSumaK,
  productoExceptoSiMismo, moverCeros, fusionarOrdenadas, tresSuma, contenedorMasAgua,
  maxSumaVentana, subcadenaSinRepetir, evaluarRpn, temperaturasDiarias, PilaMinima,
  raizEntera, buscarEnRotado, invertirLista, tieneCiclo, alturaArbol, recorridoPorNiveles,
  esBstValido, contarIslas, ordenCursos, subconjuntos, permutaciones, formasSubirEscalera,
  maxSubarreglo, subsecuenciaComunMasLarga, mergeSort, CacheLRU,
};
