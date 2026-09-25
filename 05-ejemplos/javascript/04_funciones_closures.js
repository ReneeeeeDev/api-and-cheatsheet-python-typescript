// 04 - Funciones: declaración vs expresión, arrow, parámetros, closures, this, recursión, errores.
// Ejecutar:  node 04_funciones_closures.js

// ---------------------------------------------------------------- FORMAS DE DECLARAR
function sumar(a, b = 0) { return a + b; }            // declaración (hoisting: se puede usar antes)
const restar = function (a, b) { return a - b; };     // expresión
const multiplicar = (a, b) => a * b;                  // arrow: return implícito
const crearObjeto = (n) => ({ nombre: n });           // arrow devolviendo objeto → paréntesis
console.log(sumar(2), restar(5, 3), multiplicar(3, 4), crearObjeto("Ana"));

// Parámetros rest y spread
const promedio = (...nums) => nums.reduce((s, n) => s + n, 0) / nums.length;
console.log(promedio(8, 9, 10), Math.max(...[3, 9, 1]));

// Parámetros con destructuring (muy usado en React)
function crearUsuario({ nombre, rol = "estudiante", activo = true } = {}) {
  return `${nombre} (${rol}) ${activo ? "activo" : "inactivo"}`;
}
console.log(crearUsuario({ nombre: "Ana" }), crearUsuario({ nombre: "Luis", rol: "docente" }));

// Funciones como valores (callbacks)
const operar = (a, b, operacion) => operacion(a, b);
console.log(operar(6, 3, multiplicar), operar(6, 3, (x, y) => x / y));

// ---------------------------------------------------------------- CLOSURES
function crearContador(inicial = 0) {
  let cuenta = inicial;                     // variable "privada"
  return {
    incrementar: () => ++cuenta,
    decrementar: () => --cuenta,
    valor: () => cuenta,
  };
}
const c = crearContador(10);
c.incrementar(); c.incrementar(); c.decrementar();
console.log("contador:", c.valor());       // 11

// Fábrica de funciones
const multiplicarPor = (factor) => (n) => n * factor;
const doble = multiplicarPor(2), triple = multiplicarPor(3);
console.log(doble(5), triple(5));

// Memoización
function memoizar(fn) {
  const cache = new Map();
  return (n) => {
    if (!cache.has(n)) cache.set(n, fn(n));
    return cache.get(n);
  };
}
const fib = memoizar((n) => (n < 2 ? n : fib(n - 1) + fib(n - 2)));
console.log("fib(80):", fib(80));

// Debounce (esperar a que el usuario deje de escribir)
function debounce(fn, ms) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}
const buscar = debounce((texto) => console.log("buscando:", texto), 50);
buscar("h"); buscar("ho"); buscar("hola");          // solo imprime "buscando: hola"

// ---------------------------------------------------------------- THIS
const objeto = {
  nombre: "Objeto",
  normal() { return this.nombre; },                // this = el objeto
  flecha: () => typeof this,                       // arrow NO tiene su propio this
  conTimer() {
    setTimeout(() => console.log("this en arrow dentro de método:", this.nombre), 0);
  },
};
console.log(objeto.normal(), objeto.flecha());
objeto.conTimer();
const suelta = objeto.normal;
console.log("método suelto:", suelta());   // undefined: perdió su this (en modo estricto sería un error)
const ligada = objeto.normal.bind(objeto);
console.log("con bind:", ligada());

// ---------------------------------------------------------------- RECURSIÓN
const factorial = (n) => (n <= 1 ? 1 : n * factorial(n - 1));
const aplanar = (arr) => arr.reduce((acc, x) => acc.concat(Array.isArray(x) ? aplanar(x) : x), []);
function permutaciones(s) {
  if (s.length <= 1) return [s];
  return [...s].flatMap((c, i) => permutaciones(s.slice(0, i) + s.slice(i + 1)).map((p) => c + p));
}
console.log(factorial(10), aplanar([1, [2, [3, [4]]]]), permutaciones("abc"));

// ---------------------------------------------------------------- ERRORES
class ValidacionError extends Error {
  constructor(campo, mensaje) {
    super(mensaje);
    this.name = "ValidacionError";
    this.campo = campo;
  }
}
function validarEdad(edad) {
  if (typeof edad !== "number" || Number.isNaN(edad)) throw new TypeError("La edad debe ser un número");
  if (edad < 0 || edad > 120) throw new ValidacionError("edad", "Edad fuera de rango");
  return true;
}
for (const valor of [25, -1, "x"]) {
  try {
    validarEdad(valor);
    console.log(valor, "válida");
  } catch (e) {
    if (e instanceof ValidacionError) console.log(`Campo ${e.campo}: ${e.message}`);
    else console.log(`${e.name}: ${e.message}`);
  } finally {
    // siempre se ejecuta
  }
}

// Errores comunes:
// ReferenceError: x is not defined          → variable no declarada / typo
// TypeError: Cannot read properties of undefined (reading 'x')  → objeto undefined: usa ?.
// TypeError: x is not a function            → llamaste algo que no es función
// SyntaxError: Unexpected token             → falta ) } , o JSON mal formado
