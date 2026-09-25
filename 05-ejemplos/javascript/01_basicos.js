// 01 - Variables, tipos, operadores, conversiones y control de flujo.
// Ejecutar:  node 01_basicos.js

// ---------------------------------------------------------------- VARIABLES
const nombre = "Ana";        // no se puede reasignar (úsala por defecto)
let edad = 25;               // se puede reasignar
// var  → NO usar (ámbito de función, hoisting confuso)

console.log(typeof nombre, typeof edad, typeof true, typeof undefined, typeof null, typeof {}, typeof []);
// string number boolean undefined object object object   (null y [] dicen "object": rarezas de JS)
console.log(Array.isArray([]));                            // true (la forma correcta de detectar arrays)

// ---------------------------------------------------------------- OPERADORES
console.log(7 + 2, 7 - 2, 7 * 2, 7 / 2, 7 % 2, 2 ** 10);    // 9 5 14 3.5 1 1024
console.log(Math.floor(7 / 2), Math.trunc(-3.5), Math.round(2.5), Math.round(-2.5)); // 3 -3 3 -2
console.log(0.1 + 0.2, (0.1 + 0.2).toFixed(2), 0.1 + 0.2 === 0.3); // 0.30000000000000004 "0.30" false

// Igualdad: SIEMPRE ===
console.log("5" == 5, "5" === 5, null == undefined, null === undefined, NaN === NaN); // true false true false false

// Truthy / falsy: son falsy → false, 0, "", null, undefined, NaN
console.log(Boolean(""), Boolean("0"), Boolean([]), Boolean(0), !!"hola");  // false true true false true

// Lógicos que devuelven valores
const usuario = null;
console.log(usuario || "Invitado");      // "Invitado"  (|| usa el derecho si el izquierdo es falsy)
console.log(0 || 10, 0 ?? 10);           // 10 0        (?? solo si es null/undefined)
const config = { tema: { color: "azul" } };
console.log(config?.tema?.color, config?.fuente?.tamano);   // azul undefined (sin error)

// ---------------------------------------------------------------- CONVERSIONES
console.log(Number("42"), Number(""), Number("abc"), parseInt("42px"), parseFloat("3.5kg")); // 42 0 NaN 42 3.5
console.log(String(10) + 1, 10 + 1 + "1", "3" * "4", "3" + 4);   // "101" "111" 12 "34"
console.log(Number.isNaN(Number("abc")), Number.isInteger(5.0), (1234.5678).toFixed(2));
console.log((1234567.891).toLocaleString("es-EC", { style: "currency", currency: "USD" }));

// ---------------------------------------------------------------- TEMPLATE STRINGS
const precio = 12.5;
console.log(`Hola ${nombre}, en 5 años tendrás ${edad + 5}. Total: $${(precio * 3).toFixed(2)}`);
const multilinea = `Línea 1
Línea 2`;
console.log(multilinea);

// ---------------------------------------------------------------- CONDICIONALES
const nota = 8.4;
if (nota >= 9) console.log("Excelente");
else if (nota >= 7) console.log("Aprobado");
else console.log("Reprobado");

console.log(edad >= 18 ? "Mayor" : "Menor");

const dia = 3;
switch (dia) {
  case 1:
  case 7:
    console.log("Fin de semana");
    break;
  case 2: case 3: case 4: case 5: case 6:
    console.log("Laborable");
    break;                     // ¡sin break sigue al siguiente case!
  default:
    console.log("Inválido");
}

// ---------------------------------------------------------------- BUCLES
for (let i = 0; i < 3; i++) console.log("for", i);

const frutas = ["pera", "uva", "kiwi"];
for (const f of frutas) console.log("of", f);             // valores (arrays, strings)
for (const i in frutas) console.log("in", i);             // índices/claves (mejor para objetos)
for (const [i, f] of frutas.entries()) console.log(i, f);

let n = 5, suma = 0;
while (n > 0) { suma += n; n--; }
console.log("suma", suma);

let intentos = 0;
do { intentos++; } while (intentos < 3);
console.log("intentos", intentos);

// break y continue
for (const x of [3, 8, 11, 4]) {
  if (x % 2 === 0) continue;
  if (x > 10) { console.log("encontré", x); break; }
}

// Etiquetas para romper bucles anidados
externo: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (i * j === 2) { console.log("rompo en", i, j); break externo; }
  }
}

// ---------------------------------------------------------------- ENTRADA POR CONSOLA (Node)
// import readline from "readline/promises";   (en archivos .mjs o con "type": "module")
// const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
// const texto = await rl.question("Número: ");
// rl.close();
// Argumentos:  node 01_basicos.js 5 hola   →  process.argv = [node, archivo, "5", "hola"]
console.log("argumentos:", process.argv.slice(2));
