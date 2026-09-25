// 03 - Objetos, JSON, Map/Set y cadenas de texto.
// Ejecutar:  node 03_objetos_strings.js

// ---------------------------------------------------------------- OBJETOS
const persona = {
  nombre: "Ana",
  edad: 25,
  direccion: { ciudad: "Ambato", calle: "Av. Cevallos" },
  saludar() { return `Hola, soy ${this.nombre}`; },   // método
};

persona.email = "ana@mail.com";                  // agregar
persona["telefono"] = "0987654321";              // notación de corchetes (clave dinámica)
delete persona.telefono;                         // eliminar
console.log(persona.saludar(), persona.direccion.ciudad, "email" in persona, persona.hasOwnProperty("edad"));

const { nombre, edad: años, direccion: { ciudad }, pais = "Ecuador" } = persona;   // destructuring con renombre y defecto
console.log(nombre, años, ciudad, pais);

const clave = "rol";
const usuario = { ...persona, [clave]: "admin", edad: 26 };   // spread + clave calculada + sobrescribir
console.log(usuario.rol, usuario.edad, persona.edad);         // admin 26 25

console.log(Object.keys(persona), Object.values({ a: 1, b: 2 }), Object.entries({ a: 1, b: 2 }));
for (const [k, v] of Object.entries({ x: 1, y: 2 })) console.log(k, "=", v);

// Copia superficial vs profunda
const copiaSuperficial = { ...persona };
copiaSuperficial.direccion.ciudad = "Quito";              // ¡modifica también el original!
console.log(persona.direccion.ciudad);                    // Quito
const copiaProfunda = structuredClone(persona.direccion);  // Node 17+: copia real
copiaProfunda.ciudad = "Cuenca";
console.log(persona.direccion.ciudad);                    // Quito (no cambió)

// Congelar
const CONFIG = Object.freeze({ IVA: 0.15 });
// CONFIG.IVA = 0.12;  → se ignora (en modo estricto da error)

// ---------------------------------------------------------------- JSON
const texto = JSON.stringify({ nombre: "Ana", notas: [9, 10], activo: true, fecha: new Date(0) });
console.log(texto);
const objeto = JSON.parse(texto);
console.log(objeto.notas[1], typeof objeto.fecha);        // 10 "string" (las fechas se vuelven texto)
console.log(JSON.stringify({ a: 1, b: [1, 2] }, null, 2));  // con sangría
try { JSON.parse("{mal json}"); } catch (e) { console.log("JSON inválido:", e.name); }

// ---------------------------------------------------------------- MAP Y SET
const stock = new Map();
stock.set("mouse", 10).set("teclado", 3);
console.log(stock.get("mouse"), stock.has("monitor"), stock.size);
for (const [prod, cant] of stock) console.log(prod, cant);

const vistos = new Set([1, 2, 2, 3]);
vistos.add(4); vistos.delete(1);
console.log(vistos.has(2), vistos.size, [...vistos]);

// ---------------------------------------------------------------- STRINGS
const s = "  Hola Mundo JavaScript  ";
console.log(s.trim(), s.trimStart().length, s.toLowerCase(), s.toUpperCase());
console.log(s.includes("Mundo"), s.trim().startsWith("Hola"), s.trim().endsWith("Script"));
console.log(s.indexOf("o"), s.lastIndexOf("o"), s.trim().slice(0, 4), s.trim().slice(-6));
console.log(s.trim().split(" "), "a,b,,c".split(","), ["2026", "09", "25"].join("-"));
console.log(s.replace("o", "0"), s.replaceAll("o", "0"), "ja".repeat(3), "7".padStart(3, "0"));
console.log("hola"[0], "hola".at(-1), "hola".charCodeAt(0), String.fromCharCode(72));
console.log([..."hola"].reverse().join(""));             // invertir

const quitarTildes = (t) => t.normalize("NFD").replace(/[̀-ͯ]/g, "");
console.log(quitarTildes("Canción, pingüino, Ñandú"));   // Cancion, pinguino, Nandu

const capitalizar = (t) => t.toLowerCase().replace(/\b\p{L}/gu, (c) => c.toUpperCase());
console.log(capitalizar("iNSTITUTO tecnológico ESPAÑA"));

const esPalindromo = (t) => {
  const l = quitarTildes(t.toLowerCase()).replace(/[^a-z0-9]/g, "");
  return l === [...l].reverse().join("");
};
console.log(esPalindromo("Anita lava la tina"), esPalindromo("Ecuador"));

const iniciales = (n) => n.split(" ").map((p) => p[0].toUpperCase() + ".").join("");
console.log(iniciales("juan carlos pérez"));

const slug = (t) => quitarTildes(t.toLowerCase()).trim().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
console.log(slug("  Técnico en Desarrollo de Software (Junior)! "));   // tecnico-en-desarrollo-de-software-junior

// Comparar ignorando mayúsculas y tildes
console.log("árbol".localeCompare("ARBOL", "es", { sensitivity: "base" }) === 0);   // true
