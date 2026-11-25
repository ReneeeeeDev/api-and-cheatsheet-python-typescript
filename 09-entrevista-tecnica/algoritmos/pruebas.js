// Pruebas de los 30 problemas de PROBLEMAS.md (JavaScript).
//
// Uso (desde esta carpeta):
//   node pruebas.js                          → prueba las soluciones de referencia
//   node pruebas.js mis_soluciones.js        → prueba TU archivo (copia plantilla.js → mis_soluciones.js)
//   node pruebas.js mis_soluciones.js 7 12   → solo los problemas 7 y 12
//
// Las funciones que siguen lanzando "pendiente" aparecen como PENDIENTE.
const path = require("node:path");
const { crearLista, listaAArray, crearArbol } = require("./estructuras");

const PRUEBAS = [];
const prueba = (numero, nombre, fn) => PRUEBAS.push({ numero, nombre, fn });

// JSON.stringify compara arreglos y números (trata -0 como 0).
function igual(obtenido, esperado) {
  if (JSON.stringify(obtenido) !== JSON.stringify(esperado)) {
    throw new Error(`se esperaba ${JSON.stringify(esperado)}, se obtuvo ${JSON.stringify(obtenido)}`);
  }
}

// Para resultados cuyo orden no importa (tripletas, subconjuntos).
const normalizar = (listas) =>
  listas.map((x) => [...x].sort((a, b) => a - b)).sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));

// ---------------------------------------------------------------- A. hash
prueba(1, "contieneDuplicado", (m) => {
  igual(m.contieneDuplicado([1, 2, 3, 1]), true);
  igual(m.contieneDuplicado([1, 2, 3, 4]), false);
  igual(m.contieneDuplicado([]), false);
});

prueba(2, "elementoMayoritario", (m) => {
  igual(m.elementoMayoritario([3, 2, 3]), 3);
  igual(m.elementoMayoritario([2, 2, 1, 1, 1, 2, 2]), 2);
  igual(m.elementoMayoritario([1, 5, 5]), 5);
  igual(m.elementoMayoritario([7]), 7);
});

prueba(3, "secuenciaConsecutivaMasLarga", (m) => {
  igual(m.secuenciaConsecutivaMasLarga([100, 4, 200, 1, 3, 2]), 4);
  igual(m.secuenciaConsecutivaMasLarga([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9);
  igual(m.secuenciaConsecutivaMasLarga([]), 0);
});

prueba(4, "subarreglosSumaK", (m) => {
  igual(m.subarreglosSumaK([1, 1, 1], 2), 2);
  igual(m.subarreglosSumaK([1, 2, 3], 3), 2);
  igual(m.subarreglosSumaK([1, -1, 0], 0), 3);
});

prueba(5, "productoExceptoSiMismo", (m) => {
  igual(m.productoExceptoSiMismo([1, 2, 3, 4]), [24, 12, 8, 6]);
  igual(m.productoExceptoSiMismo([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0]);
  igual(m.productoExceptoSiMismo([0, 1, 2]), [2, 0, 0]);
});

// ----------------------------------------------------------- B. punteros
prueba(6, "moverCeros", (m) => {
  let nums = [0, 1, 0, 3, 12];
  m.moverCeros(nums);
  igual(nums, [1, 3, 12, 0, 0]); // debe modificar el mismo arreglo
  nums = [0, 0, 1];
  m.moverCeros(nums);
  igual(nums, [1, 0, 0]);
});

prueba(7, "fusionarOrdenadas", (m) => {
  igual(m.fusionarOrdenadas([1, 3, 5], [2, 4]), [1, 2, 3, 4, 5]);
  igual(m.fusionarOrdenadas([], [1]), [1]);
  igual(m.fusionarOrdenadas([1, 1], [1]), [1, 1, 1]);
});

prueba(8, "tresSuma", (m) => {
  igual(normalizar(m.tresSuma([-1, 0, 1, 2, -1, -4])), [[-1, -1, 2], [-1, 0, 1]]);
  igual(normalizar(m.tresSuma([0, 0, 0, 0])), [[0, 0, 0]]);
  igual(m.tresSuma([1, 2, 3]), []);
});

prueba(9, "contenedorMasAgua", (m) => {
  igual(m.contenedorMasAgua([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
  igual(m.contenedorMasAgua([1, 1]), 1);
});

// ------------------------------------------------------------- C. ventana
prueba(10, "maxSumaVentana", (m) => {
  igual(m.maxSumaVentana([2, 1, 5, 1, 3, 2], 3), 9);
  igual(m.maxSumaVentana([-1, -2, -3], 2), -3);
  igual(m.maxSumaVentana([1, 2], 3), null);
});

prueba(11, "subcadenaSinRepetir", (m) => {
  igual(m.subcadenaSinRepetir("abcabcbb"), 3);
  igual(m.subcadenaSinRepetir("bbbbb"), 1);
  igual(m.subcadenaSinRepetir("pwwkew"), 3);
  igual(m.subcadenaSinRepetir("abba"), 2);
  igual(m.subcadenaSinRepetir(""), 0);
});

// --------------------------------------------------------------- D. pilas
prueba(12, "evaluarRpn", (m) => {
  igual(m.evaluarRpn(["2", "1", "+", "3", "*"]), 9);
  igual(m.evaluarRpn(["4", "13", "5", "/", "+"]), 6);
  igual(m.evaluarRpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22);
});

prueba(13, "temperaturasDiarias", (m) => {
  igual(m.temperaturasDiarias([73, 74, 75, 71, 69, 72, 76, 73]), [1, 1, 4, 2, 1, 1, 0, 0]);
  igual(m.temperaturasDiarias([30, 60, 90]), [1, 1, 0]);
  igual(m.temperaturasDiarias([90, 60, 30]), [0, 0, 0]);
});

prueba(14, "PilaMinima", (m) => {
  const p = new m.PilaMinima();
  p.apilar(5);
  p.apilar(3);
  p.apilar(7);
  p.apilar(3);
  igual(p.minimo(), 3);
  igual(p.desapilar(), 3);
  igual(p.minimo(), 3);
  p.desapilar();
  p.desapilar();
  igual(p.minimo(), 5);
  igual(p.tope(), 5);
});

// ---------------------------------------------------- E. búsqueda binaria
prueba(15, "raizEntera", (m) => {
  for (const [n, esperado] of [[0, 0], [1, 1], [8, 2], [16, 4], [99, 9], [2147395599, 46339]]) {
    igual(m.raizEntera(n), esperado);
  }
});

prueba(16, "buscarEnRotado", (m) => {
  igual(m.buscarEnRotado([4, 5, 6, 7, 0, 1, 2], 0), 4);
  igual(m.buscarEnRotado([4, 5, 6, 7, 0, 1, 2], 3), -1);
  igual(m.buscarEnRotado([1], 0), -1);
  igual(m.buscarEnRotado([3, 1], 1), 1);
  igual(m.buscarEnRotado([5, 1, 3], 5), 0);
});

// ------------------------------------------------------ F. listas enlazadas
prueba(17, "invertirLista", (m) => {
  igual(listaAArray(m.invertirLista(crearLista([1, 2, 3, 4]))), [4, 3, 2, 1]);
  igual(listaAArray(m.invertirLista(crearLista([1]))), [1]);
  igual(m.invertirLista(null), null);
});

prueba(18, "tieneCiclo", (m) => {
  const cabeza = crearLista([3, 2, 0, -4]);
  cabeza.siguiente.siguiente.siguiente.siguiente = cabeza.siguiente; // -4 apunta a 2
  igual(m.tieneCiclo(cabeza), true);
  igual(m.tieneCiclo(crearLista([1, 2, 3])), false);
  igual(m.tieneCiclo(null), false);
});

// ------------------------------------------------------------- G. árboles
prueba(19, "alturaArbol", (m) => {
  igual(m.alturaArbol(crearArbol([3, 9, 20, null, null, 15, 7])), 3);
  igual(m.alturaArbol(crearArbol([1, null, 2])), 2);
  igual(m.alturaArbol(null), 0);
});

prueba(20, "recorridoPorNiveles", (m) => {
  igual(m.recorridoPorNiveles(crearArbol([3, 9, 20, null, null, 15, 7])), [[3], [9, 20], [15, 7]]);
  igual(m.recorridoPorNiveles(crearArbol([1])), [[1]]);
  igual(m.recorridoPorNiveles(null), []);
});

prueba(21, "esBstValido", (m) => {
  igual(m.esBstValido(crearArbol([2, 1, 3])), true);
  igual(m.esBstValido(crearArbol([5, 1, 4, null, null, 3, 6])), false);
  igual(m.esBstValido(crearArbol([5, 4, 6, null, null, 3, 7])), false); // 3 < 5 en el lado derecho
  igual(m.esBstValido(null), true);
});

// --------------------------------------------------------------- H. grafos
prueba(22, "contarIslas", (m) => {
  const mapa = ["11000",
                "11000",
                "00100",
                "00011"];
  igual(m.contarIslas(mapa), 3);
  igual(m.contarIslas(["111", "010", "111"]), 1);
  igual(m.contarIslas(["000"]), 0);
});

prueba(23, "ordenCursos", (m) => {
  const pre = [[1, 0], [2, 0], [3, 1], [3, 2]];
  const orden = m.ordenCursos(4, pre);
  const posicion = new Map(orden.map((materia, i) => [materia, i]));
  const valido = [...orden].sort().join() === "0,1,2,3" &&
    pre.every(([mat, req]) => posicion.get(req) < posicion.get(mat));
  if (!valido) throw new Error(`orden no válido: ${JSON.stringify(orden)}`);
  igual(m.ordenCursos(2, [[1, 0], [0, 1]]), []); // ciclo
  igual([...m.ordenCursos(3, [])].sort(), [0, 1, 2]);
});

// --------------------------------------------------------- I. backtracking
prueba(24, "subconjuntos", (m) => {
  igual(normalizar(m.subconjuntos([1, 2, 3])),
    normalizar([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]));
  igual(m.subconjuntos([]), [[]]);
});

prueba(25, "permutaciones", (m) => {
  const obtenido = m.permutaciones([1, 2, 3]).map((p) => p.join("")).sort();
  igual(obtenido, ["123", "132", "213", "231", "312", "321"]);
  igual(m.permutaciones([1]), [[1]]);
});

// ------------------------------------------------ J. programación dinámica
prueba(26, "formasSubirEscalera", (m) => {
  for (const [n, esperado] of [[1, 1], [2, 2], [3, 3], [5, 8], [45, 1836311903]]) {
    igual(m.formasSubirEscalera(n), esperado);
  }
});

prueba(27, "maxSubarreglo", (m) => {
  igual(m.maxSubarreglo([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6);
  igual(m.maxSubarreglo([-3, -1, -2]), -1);
  igual(m.maxSubarreglo([5]), 5);
});

prueba(28, "subsecuenciaComunMasLarga", (m) => {
  igual(m.subsecuenciaComunMasLarga("abcde", "ace"), 3);
  igual(m.subsecuenciaComunMasLarga("abc", "abc"), 3);
  igual(m.subsecuenciaComunMasLarga("abc", "def"), 0);
});

// ------------------------------------------------ K. ordenamiento y diseño
prueba(29, "mergeSort", (m) => {
  const original = [5, 2, 9, 1, 5, 6];
  igual(m.mergeSort(original), [1, 2, 5, 5, 6, 9]);
  igual(original, [5, 2, 9, 1, 5, 6]); // no debe modificar la entrada
  igual(m.mergeSort([]), []);
});

prueba(30, "CacheLRU", (m) => {
  const c = new m.CacheLRU(2);
  c.poner(1, 1);
  c.poner(2, 2);
  igual(c.obtener(1), 1);
  c.poner(3, 3); // expulsa la clave 2 (la usada hace más tiempo)
  igual(c.obtener(2), -1);
  c.poner(4, 4); // expulsa la clave 1
  igual(c.obtener(1), -1);
  igual(c.obtener(3), 3);
  igual(c.obtener(4), 4);
});

// ----------------------------------------------------------------- runner
const archivo = process.argv[2] ?? "soluciones.js";
const solo = new Set(process.argv.slice(3).map(Number));
const modulo = require(path.resolve(__dirname, archivo));
const conteo = { OK: 0, FALLO: 0, PENDIENTE: 0 };
console.log(`Probando ${archivo}\n`);
for (const { numero, nombre, fn } of PRUEBAS) {
  if (solo.size && !solo.has(numero)) continue;
  let estado = "OK";
  let detalle = "";
  if (!(nombre in modulo)) {
    estado = "PENDIENTE";
    detalle = `(no se exporta ${nombre})`;
  } else {
    try {
      fn(modulo);
    } catch (e) {
      if (e.message === "pendiente") estado = "PENDIENTE";
      else {
        estado = "FALLO";
        detalle = `${e.name}: ${e.message}`;
      }
    }
  }
  conteo[estado]++;
  console.log(`${String(numero).padStart(2)}. ${nombre.padEnd(30)} ${estado.padEnd(9)} ${detalle}`);
}
const total = conteo.OK + conteo.FALLO + conteo.PENDIENTE;
console.log(`\n${conteo.OK}/${total} correctas | ${conteo.FALLO} con fallos | ${conteo.PENDIENTE} pendientes`);
process.exitCode = conteo.OK === total ? 0 : 1;
