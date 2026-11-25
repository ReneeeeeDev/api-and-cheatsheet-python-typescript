// Soluciones de los 30 ejercicios en JavaScript. Ejecutar: node soluciones.js

// ---------------------------------------------------------------- NIVEL 1
const esPar = (n) => n % 2 === 0;

function mayorDeTres(a, b, c) {
  let mayor = a;
  if (b > mayor) mayor = b;
  if (c > mayor) mayor = c;
  return mayor;
}

function factorial(n) {
  let r = 1;
  for (let i = 2; i <= n; i++) r *= i;
  return r;
}
const factorialRec = (n) => (n <= 1 ? 1 : n * factorialRec(n - 1));

function sumaDigitos(n) {
  let total = 0;
  n = Math.abs(n);
  while (n > 0) { total += n % 10; n = Math.floor(n / 10); }
  return total;
}

function invertirTexto(s) {
  let r = "";
  for (const c of s) r = c + r;
  return r;
}

const quitarTildes = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "");

const contarVocales = (s) => [...quitarTildes(s.toLowerCase())].filter((c) => "aeiou".includes(c)).length;

const tablaMultiplicar = (n) => Array.from({ length: 10 }, (_, i) => n * (i + 1));

const celsiusAFahrenheit = (c) => (c * 9) / 5 + 32;

const esBisiesto = (a) => (a % 4 === 0 && a % 100 !== 0) || a % 400 === 0;

function fizzbuzz(n) {
  const r = [];
  for (let i = 1; i <= n; i++) {
    if (i % 15 === 0) r.push("FizzBuzz");
    else if (i % 3 === 0) r.push("Fizz");
    else if (i % 5 === 0) r.push("Buzz");
    else r.push(i);
  }
  return r;
}

// ---------------------------------------------------------------- NIVEL 2
function esPrimo(n) {
  if (n < 2) return false;
  for (let d = 2; d * d <= n; d++) if (n % d === 0) return false;
  return true;
}

function fibonacci(n) {
  const serie = [];
  let [a, b] = [0, 1];
  for (let i = 0; i < n; i++) { serie.push(a); [a, b] = [b, a + b]; }
  return serie;
}

function esPalindromo(s) {
  const limpio = quitarTildes(s.toLowerCase()).replace(/[^a-z0-9ñ]/g, "");
  return limpio === [...limpio].reverse().join("");
}

function contarPalabras(texto) {
  const conteo = {};
  for (const p of quitarTildes(texto.toLowerCase()).match(/\w+/g) ?? []) conteo[p] = (conteo[p] || 0) + 1;
  return conteo;
}

function segundoMayor(lista) {
  const unicos = [...new Set(lista)].sort((a, b) => b - a);
  return unicos.length >= 2 ? unicos[1] : null;
}

const eliminarDuplicados = (lista) => [...new Set(lista)];   // Set mantiene el orden de inserción

function sonAnagramas(a, b) {
  const normal = (s) => [...quitarTildes(s.toLowerCase().replaceAll(" ", ""))].sort().join("");
  return normal(a) === normal(b);
}

function mcd(a, b) {
  while (b) [a, b] = [b, a % b];
  return a;
}
const mcm = (a, b) => (a * b) / mcd(a, b);

function decimalABinario(n) {
  if (n === 0) return "0";
  let bits = "";
  while (n > 0) { bits = (n % 2) + bits; n = Math.floor(n / 2); }
  return bits;
}

function validarCedula(cedula) {
  if (!/^\d{10}$/.test(cedula)) return false;
  const provincia = Number(cedula.slice(0, 2));
  if (!((provincia >= 1 && provincia <= 24) || provincia === 30) || Number(cedula[2]) >= 6) return false;
  const coef = [2, 1, 2, 1, 2, 1, 2, 1, 2];
  const suma = coef.reduce((acc, c, i) => {
    const p = Number(cedula[i]) * c;
    return acc + (p > 9 ? p - 9 : p);
  }, 0);
  return (10 - (suma % 10)) % 10 === Number(cedula[9]);
}

// ---------------------------------------------------------------- NIVEL 3
function busquedaBinaria(lista, x) {
  let izq = 0, der = lista.length - 1;
  while (izq <= der) {
    const medio = Math.floor((izq + der) / 2);
    if (lista[medio] === x) return medio;
    if (lista[medio] < x) izq = medio + 1;
    else der = medio - 1;
  }
  return -1;
}

function ordenarBurbuja(lista) {
  const a = [...lista];
  for (let i = 0; i < a.length - 1; i++) {
    let cambio = false;
    for (let j = 0; j < a.length - 1 - i; j++) {
      if (a[j] > a[j + 1]) { [a[j], a[j + 1]] = [a[j + 1], a[j]]; cambio = true; }
    }
    if (!cambio) break;
  }
  return a;
}

function parentesisBalanceados(s) {
  const pares = { ")": "(", "]": "[", "}": "{" };
  const pila = [];
  for (const c of s) {
    if ("([{".includes(c)) pila.push(c);
    else if (c in pares && pila.pop() !== pares[c]) return false;
  }
  return pila.length === 0;
}

function comprimir(s) {
  let r = "";
  for (let i = 0, cuenta = 1; i < s.length; i++, cuenta++) {
    if (s[i] !== s[i + 1]) { r += s[i] + cuenta; cuenta = 0; }
  }
  return r;
}

const rotarMatriz = (m) => m[0].map((_, c) => m.map((fila) => fila[c]).reverse());

function dosSuma(nums, objetivo) {
  const vistos = new Map();
  for (let i = 0; i < nums.length; i++) {
    const falta = objetivo - nums[i];
    if (vistos.has(falta)) return [vistos.get(falta), i];
    vistos.set(nums[i], i);
  }
  return null;
}

function numeroRomano(n) {
  const tabla = [[1000, "M"], [900, "CM"], [500, "D"], [400, "CD"], [100, "C"], [90, "XC"],
    [50, "L"], [40, "XL"], [10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"]];
  let r = "";
  for (const [valor, simbolo] of tabla) while (n >= valor) { r += simbolo; n -= valor; }
  return r;
}

const agruparPor = (registros, clave) =>
  registros.reduce((acc, r) => ((acc[r[clave]] ||= []).push(r), acc), {});

function calcularNomina(empleados, tasa = 0.0945) {
  const redondear = (x) => Math.round(x * 100) / 100;
  const detalle = empleados.map((e) => {
    const aporte = redondear(e.sueldo * tasa);
    return { nombre: e.nombre, aporte, neto: redondear(e.sueldo - aporte) };
  });
  const total = redondear(detalle.reduce((s, d) => s + d.neto, 0));
  return { detalle, total };
}

function cajero(monto, denominaciones = [20, 10, 5, 1]) {
  const r = {};
  for (const d of denominaciones) {
    const cantidad = Math.floor(monto / d);
    if (cantidad) { r[d] = cantidad; monto %= d; }
  }
  return r;
}

// ---------------------------------------------------------------- PRUEBAS
const igual = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const casos = [
  [esPar(4) && !esPar(7), "esPar"],
  [mayorDeTres(3, 9, 5) === 9, "mayorDeTres"],
  [factorial(5) === 120 && factorialRec(5) === 120, "factorial"],
  [sumaDigitos(1234) === 10, "sumaDigitos"],
  [invertirTexto("hola") === "aloh", "invertirTexto"],
  [contarVocales("Murciélago") === 5, "contarVocales"],
  [tablaMultiplicar(3)[9] === 30, "tablaMultiplicar"],
  [celsiusAFahrenheit(100) === 212, "celsiusAFahrenheit"],
  [esBisiesto(2024) && !esBisiesto(1900) && esBisiesto(2000), "esBisiesto"],
  [fizzbuzz(15)[14] === "FizzBuzz" && fizzbuzz(5)[2] === "Fizz", "fizzbuzz"],
  [igual([...Array(20).keys()].filter(esPrimo), [2, 3, 5, 7, 11, 13, 17, 19]), "esPrimo"],
  [igual(fibonacci(7), [0, 1, 1, 2, 3, 5, 8]), "fibonacci"],
  [esPalindromo("Anita lava la tina") && !esPalindromo("hola"), "esPalindromo"],
  [igual(contarPalabras("Hola, hola mundo!"), { hola: 2, mundo: 1 }), "contarPalabras"],
  [segundoMayor([4, 9, 9, 2]) === 4 && segundoMayor([1, 1]) === null, "segundoMayor"],
  [igual(eliminarDuplicados([3, 1, 3, 2, 1]), [3, 1, 2]), "eliminarDuplicados"],
  [sonAnagramas("Roma", "amor") && !sonAnagramas("abc", "abd"), "sonAnagramas"],
  [mcd(48, 18) === 6 && mcm(4, 6) === 12, "mcd/mcm"],
  [decimalABinario(10) === "1010", "decimalABinario"],
  [validarCedula("1710034065") && !validarCedula("1710034064"), "validarCedula"],
  [busquedaBinaria([1, 3, 5, 7, 9], 7) === 3 && busquedaBinaria([1, 3], 4) === -1, "busquedaBinaria"],
  [igual(ordenarBurbuja([5, 2, 9, 1]), [1, 2, 5, 9]), "ordenarBurbuja"],
  [parentesisBalanceados("({[]})") && !parentesisBalanceados("([)]"), "parentesis"],
  [comprimir("aaabbc") === "a3b2c1", "comprimir"],
  [igual(rotarMatriz([[1, 2], [3, 4]]), [[3, 1], [4, 2]]), "rotarMatriz"],
  [igual(dosSuma([2, 7, 11, 15], 9), [0, 1]), "dosSuma"],
  [numeroRomano(1994) === "MCMXCIV", "numeroRomano"],
  [agruparPor([{ c: "A" }, { c: "B" }, { c: "A" }], "c").A.length === 2, "agruparPor"],
  [calcularNomina([{ nombre: "Ana", sueldo: 1000 }]).total === 905.5, "calcularNomina"],
  [igual(cajero(38), { 1: 3, 5: 1, 10: 1, 20: 1 }), "cajero"],
];
casos.forEach(([ok, nombre]) => console.log((ok ? "OK    " : "FALLO ") + nombre));
console.log(`\n${casos.filter(([ok]) => ok).length}/${casos.length} correctas`);
