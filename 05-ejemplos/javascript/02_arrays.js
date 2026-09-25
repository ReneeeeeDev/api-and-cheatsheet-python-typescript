// 02 - Arrays: métodos mutables e inmutables, funciones de orden superior y CRUD en memoria.
// Ejecutar:  node 02_arrays.js

const nums = [5, 3, 8, 1];

// ---------------------------------------------------------------- MUTAN el array original
const a = [...nums];
a.push(10);           // al final        → [5,3,8,1,10]
a.unshift(0);         // al inicio       → [0,5,3,8,1,10]
a.pop();              // quita el último
a.shift();            // quita el primero
a.splice(1, 1);       // desde índice 1 quita 1          → [5,8,1]
a.splice(1, 0, 99);   // en índice 1 inserta 99          → [5,99,8,1]
a.reverse();
console.log(a);                                        // [1, 8, 99, 5]

// sort: ¡por defecto ordena como TEXTO!
console.log([10, 9, 1, 100].sort());                   // [1, 10, 100, 9]  ← mal
console.log([10, 9, 1, 100].sort((x, y) => x - y));   // [1, 9, 10, 100]  ascendente
console.log([10, 9, 1, 100].sort((x, y) => y - x));   // descendente
console.log(["pera", "Uva", "árbol"].sort((x, y) => x.localeCompare(y, "es")));   // con tildes bien

// ---------------------------------------------------------------- NO MUTAN (devuelven nuevo)
console.log(nums.slice(1, 3), nums.concat([7, 7]), [...nums, 6]);
console.log(nums.includes(8), nums.indexOf(8), nums.indexOf(99), nums.at(-1), nums.join(" - "));
console.log(nums.toSorted?.((x, y) => x - y) ?? [...nums].sort((x, y) => x - y));  // Node 20+: toSorted

// ---------------------------------------------------------------- LOS 5 IMPRESCINDIBLES
const dobles = nums.map((n) => n * 2);                       // transformar
const mayores = nums.filter((n) => n > 3);                   // filtrar
const total = nums.reduce((acc, n) => acc + n, 0);           // acumular
const primero = nums.find((n) => n > 4);                     // primer elemento que cumple
const pos = nums.findIndex((n) => n > 4);
console.log(dobles, mayores, total, primero, pos);           // [10,6,16,2] [5,8] 17 5 0
console.log(nums.some((n) => n > 7), nums.every((n) => n > 0));  // true true
nums.forEach((n, i) => process.stdout.write(`${i}:${n} `));
console.log();

// Encadenar
const resultado = [1, 2, 3, 4, 5, 6]
  .filter((n) => n % 2 === 0)
  .map((n) => n ** 2)
  .reduce((s, n) => s + n, 0);
console.log("suma de cuadrados de pares:", resultado);        // 56

// ---------------------------------------------------------------- CREAR ARRAYS
console.log(Array.from({ length: 5 }, (_, i) => i * 10));     // [0,10,20,30,40]
console.log(new Array(3).fill(0), Array.from("hola"), [...new Set([1, 1, 2, 3, 3])]);
console.log([[1, 2], [3, [4, 5]]].flat(Infinity), [1, 2].flatMap((x) => [x, x * 10]));

// Matriz
const matriz = [[1, 2, 3], [4, 5, 6]];
console.log(matriz[1][2], matriz.map((fila) => fila.reduce((s, x) => s + x, 0)));   // 6 [6, 15]
const transpuesta = matriz[0].map((_, c) => matriz.map((fila) => fila[c]));
console.log(transpuesta);

// Destructuring
const [x, y, ...resto] = [10, 20, 30, 40];
let p = 1, q = 2;
[p, q] = [q, p];                                                 // intercambio
console.log(x, y, resto, p, q);

// ---------------------------------------------------------------- ARRAY DE OBJETOS (el más usado)
let estudiantes = [
  { id: 1, nombre: "Ana", nota: 9, carrera: "Software" },
  { id: 2, nombre: "Luis", nota: 6.5, carrera: "Software" },
  { id: 3, nombre: "María", nota: 8, carrera: "Enfermería" },
];

const aprobados = estudiantes.filter((e) => e.nota >= 7).map((e) => e.nombre);
const promedio = estudiantes.reduce((s, e) => s + e.nota, 0) / estudiantes.length;
const mejor = estudiantes.reduce((m, e) => (e.nota > m.nota ? e : m));
const ordenados = [...estudiantes].sort((a, b) => b.nota - a.nota || a.nombre.localeCompare(b.nombre));
console.log(aprobados, promedio.toFixed(2), mejor.nombre, ordenados.map((e) => e.nombre));

// Agrupar por carrera
const porCarrera = estudiantes.reduce((acc, e) => {
  (acc[e.carrera] ??= []).push(e.nombre);
  return acc;
}, {});
console.log(porCarrera);                 // { Software: ['Ana','Luis'], Enfermería: ['María'] }
// Node 21+: Object.groupBy(estudiantes, e => e.carrera)

// Contar
const conteo = {};
for (const palabra of "el perro y el gato y el loro".split(" ")) conteo[palabra] = (conteo[palabra] || 0) + 1;
console.log(conteo);

// Buscar por id → objeto indexado (O(1))
const porId = Object.fromEntries(estudiantes.map((e) => [e.id, e]));
console.log(porId[3].nombre);

// ---------------------------------------------------------------- CRUD INMUTABLE (como en React)
let nextId = 4;
estudiantes = [...estudiantes, { id: nextId++, nombre: "Pedro", nota: 7.5, carrera: "Marketing" }];  // crear
estudiantes = estudiantes.map((e) => (e.id === 2 ? { ...e, nota: 7 } : e));                           // actualizar
estudiantes = estudiantes.filter((e) => e.id !== 3);                                                     // eliminar
console.table(estudiantes);                                      // tabla bonita en consola
