// Soluciones de los 20 ejercicios extra (31 a 50) en JavaScript. Ejecutar: node soluciones_extra.js

// 31 ------------------------------------------------------------------
function validarCedula(c) {
  if (!/^\d{10}$/.test(c)) return false;
  const prov = Number(c.slice(0, 2));
  if (!((prov >= 1 && prov <= 24) || prov === 30) || Number(c[2]) >= 6) return false;
  let suma = 0;
  for (let i = 0; i < 9; i++) {
    const p = Number(c[i]) * (i % 2 === 0 ? 2 : 1);
    suma += p > 9 ? p - 9 : p;
  }
  return (10 - (suma % 10)) % 10 === Number(c[9]);
}
const validarRucNatural = (ruc) => /^\d{13}$/.test(ruc) && ruc.endsWith("001") && validarCedula(ruc.slice(0, 10));

// 32 ------------------------------------------------------------------
const r2 = (x) => Math.round((x + Number.EPSILON) * 100) / 100;
function calcularFactura(items, tasaIva = 0.15, descuentoDesde = 100, descuento = 0.1) {
  const subtotal = r2(items.reduce((s, [, cant, precio]) => s + cant * precio, 0));
  const desc = subtotal > descuentoDesde ? r2(subtotal * descuento) : 0;
  const base = r2(subtotal - desc);
  const iva = r2(base * tasaIva);
  return { subtotal, descuento: desc, base, iva, total: r2(base + iva) };
}

// 33 ------------------------------------------------------------------
function estadisticas(notas) {
  const o = [...notas].sort((a, b) => a - b);
  const n = o.length, m = Math.floor(n / 2);
  const mediana = n % 2 ? o[m] : (o[m - 1] + o[m]) / 2;
  const conteo = new Map();
  o.forEach((x) => conteo.set(x, (conteo.get(x) || 0) + 1));
  const maxRep = Math.max(...conteo.values());
  const moda = Math.min(...[...conteo].filter(([, c]) => c === maxRep).map(([v]) => v));
  return { min: o[0], max: o[n - 1], promedio: r2(notas.reduce((s, x) => s + x, 0) / n), mediana, moda };
}

// 34 ------------------------------------------------------------------
const segundosAHms = (s) =>
  [Math.floor(s / 3600), Math.floor((s % 3600) / 60), s % 60].map((x) => String(x).padStart(2, "0")).join(":");

// 35 ------------------------------------------------------------------
function reservasEnConflicto(reservas) {
  const conflictos = [];
  for (let i = 0; i < reservas.length; i++)
    for (let j = i + 1; j < reservas.length; j++) {
      const [idA, labA, iniA, finA] = reservas[i];
      const [idB, labB, iniB, finB] = reservas[j];
      if (labA === labB && iniA < finB && iniB < finA) conflictos.push([idA, idB]);
    }
  return conflictos;
}

// 36 ------------------------------------------------------------------
function fusionarIntervalos(intervalos) {
  const res = [];
  for (const [ini, fin] of [...intervalos].sort((a, b) => a[0] - b[0] || a[1] - b[1])) {
    const ultimo = res.at(-1);
    if (ultimo && ini <= ultimo[1]) ultimo[1] = Math.max(ultimo[1], fin);
    else res.push([ini, fin]);
  }
  return res;
}

// 37 ------------------------------------------------------------------
function topCaracteres(texto, n = 3) {
  const conteo = {};
  for (const c of texto.toLowerCase()) if (/\p{L}/u.test(c)) conteo[c] = (conteo[c] || 0) + 1;
  return Object.entries(conteo).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, n);
}

// 38 ------------------------------------------------------------------
function matrizEspiral(n) {
  const m = Array.from({ length: n }, () => Array(n).fill(0));
  let [arriba, abajo, izq, der, v] = [0, n - 1, 0, n - 1, 1];
  while (arriba <= abajo && izq <= der) {
    for (let c = izq; c <= der; c++) m[arriba][c] = v++;
    arriba++;
    for (let f = arriba; f <= abajo; f++) m[f][der] = v++;
    der--;
    if (arriba <= abajo) { for (let c = der; c >= izq; c--) m[abajo][c] = v++; abajo--; }
    if (izq <= der) { for (let f = abajo; f >= arriba; f--) m[f][izq] = v++; izq++; }
  }
  return m;
}

// 39 ------------------------------------------------------------------
function validarPassword(clave) {
  const reglas = [
    [clave.length >= 8, "mínimo 8 caracteres"],
    [/[A-Z]/.test(clave), "una mayúscula"],
    [/[a-z]/.test(clave), "una minúscula"],
    [/\d/.test(clave), "un número"],
    [/[^A-Za-z0-9]/.test(clave), "un símbolo"],
    [!clave.includes(" "), "sin espacios"],
  ];
  return reglas.filter(([ok]) => !ok).map(([, msg]) => msg);
}

// 40 ------------------------------------------------------------------
const UNIDADES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce",
  "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós",
  "veintitrés", "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"];
const DECENAS = ["", "", "", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"];
const CENTENAS = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"];
function numeroALetras(n) {
  if (n < 30) return UNIDADES[n];
  if (n < 100) { const d = Math.floor(n / 10), u = n % 10; return DECENAS[d] + (u ? " y " + UNIDADES[u] : ""); }
  if (n === 100) return "cien";
  if (n < 1000) { const c = Math.floor(n / 100), r = n % 100; return CENTENAS[c] + (r ? " " + numeroALetras(r) : ""); }
  const miles = Math.floor(n / 1000), r = n % 1000;
  const pref = miles === 1 ? "mil" : numeroALetras(miles).replace("uno", "un") + " mil";
  return pref + (r ? " " + numeroALetras(r) : "");
}

// 41 ------------------------------------------------------------------
function multiplicarMatrices(a, b) {
  if (a[0].length !== b.length) throw new Error("Dimensiones incompatibles");
  return a.map((fila) => b[0].map((_, j) => fila.reduce((s, x, k) => s + x * b[k][j], 0)));
}

// 42 ------------------------------------------------------------------
function rotarLista(lista, k) {
  if (!lista.length) return [];
  k %= lista.length;
  return k ? [...lista.slice(-k), ...lista.slice(0, -k)] : [...lista];
}

// 43 ------------------------------------------------------------------
function agruparAnagramas(palabras) {
  const grupos = {};
  for (const p of palabras) {
    const clave = [...p.toLowerCase()].sort().join("");
    (grupos[clave] ??= []).push(p);
  }
  return Object.values(grupos).sort((a, b) => b.length - a.length || a[0].localeCompare(b[0]));
}

// 44 ------------------------------------------------------------------
function cambioMinimo(monto, monedas = [1, 5, 10, 25, 50]) {
  const min = [0, ...Array(monto).fill(Infinity)];
  for (let v = 1; v <= monto; v++)
    for (const m of monedas) if (m <= v) min[v] = Math.min(min[v], min[v - m] + 1);
  return min[monto] === Infinity ? -1 : min[monto];
}

// 45 ------------------------------------------------------------------
function fechaValida(d, m, a) {
  if (a < 1 || m < 1 || m > 12 || d < 1) return false;
  return d <= new Date(a, m, 0).getDate();          // día 0 del mes siguiente = último día del mes
}

// 46 ------------------------------------------------------------------
function diasHabilesEntre(desde, hasta, feriados = []) {   // fechas "AAAA-MM-DD"
  const f = new Set(feriados);
  let total = 0;
  const [a, m, d] = desde.split("-").map(Number);
  for (let dia = new Date(a, m - 1, d); ; dia.setDate(dia.getDate() + 1)) {
    const iso = `${dia.getFullYear()}-${String(dia.getMonth() + 1).padStart(2, "0")}-${String(dia.getDate()).padStart(2, "0")}`;
    if (iso > hasta) break;
    if (dia.getDay() !== 0 && dia.getDay() !== 6 && !f.has(iso)) total++;
  }
  return total;
}

// 47 ------------------------------------------------------------------
function cuotaPrestamo(monto, tasaAnual, meses) {
  const i = tasaAnual / 12;
  return i === 0 ? r2(monto / meses) : r2((monto * i) / (1 - (1 + i) ** -meses));
}

// 48 ------------------------------------------------------------------
function primerNoRepetido(texto) {
  const c = {};
  for (const x of texto) c[x] = (c[x] || 0) + 1;
  return [...texto].find((x) => c[x] === 1) ?? null;
}

// 49 ------------------------------------------------------------------
const reordenInventario = (productos, dias = 15) =>
  productos
    .filter((p) => p.stock < p.venta_diaria * dias)
    .map((p) => [p.codigo, p.venta_diaria * dias * 2 - p.stock])
    .sort((a, b) => b[1] - a[1]);

// 50 ------------------------------------------------------------------
function sistemaNotas(parciales, examen, asistencia) {
  const final = r2((parciales.reduce((s, x) => s + x, 0) / parciales.length) * 0.6 + examen * 0.4);
  const estado = asistencia < 70 ? "Reprobado por asistencia" : final >= 7 ? "Aprobado" : final >= 5 ? "Supletorio" : "Reprobado";
  return [final, estado];
}

// ================================================================== PRUEBAS
const igual = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const casos = [
  [validarRucNatural("1710034065001") && !validarRucNatural("1710034065002"), "31 ruc"],
  [igual(calcularFactura([["Mouse", 2, 15], ["Teclado", 1, 45]]), { subtotal: 75, descuento: 0, base: 75, iva: 11.25, total: 86.25 }), "32 factura"],
  [calcularFactura([["Monitor", 1, 200]]).total === 207, "32 descuento"],
  [igual(estadisticas([7, 9, 8, 9, 6, 7]), { min: 6, max: 9, promedio: 7.67, mediana: 7.5, moda: 7 }), "33 estadisticas"],
  [segundosAHms(3725) === "01:02:05", "34 hms"],
  [igual(reservasEnConflicto([[1, "L1", "08:00", "10:00"], [2, "L1", "09:00", "11:00"], [3, "L2", "08:00", "10:00"], [4, "L1", "10:00", "12:00"]]), [[1, 2], [2, 4]]), "35 conflictos"],
  [igual(fusionarIntervalos([[14, 15], [8, 10], [9, 12], [12, 13]]), [[8, 13], [14, 15]]), "36 fusionar"],
  [igual(topCaracteres("Desarrollo de Software"), [["e", 3], ["o", 3], ["r", 3]]), "37 top"],
  [igual(matrizEspiral(3), [[1, 2, 3], [8, 9, 4], [7, 6, 5]]), "38 espiral"],
  [validarPassword("Clave#2026").length === 0 && validarPassword("abc").length === 4, "39 password"],
  [numeroALetras(1995) === "mil novecientos noventa y cinco" && numeroALetras(21000) === "veintiun mil" && numeroALetras(115) === "ciento quince", "40 letras"],
  [igual(multiplicarMatrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]), "41 matrices"],
  [igual(rotarLista([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]) && igual(rotarLista([1, 2], 4), [1, 2]), "42 rotar"],
  [igual(agruparAnagramas(["amor", "gato", "Roma", "toga", "ramo", "sol"]), [["amor", "Roma", "ramo"], ["gato", "toga"], ["sol"]]), "43 anagramas"],
  [cambioMinimo(30, [1, 10, 25]) === 3 && cambioMinimo(63) === 5 && cambioMinimo(3, [2]) === -1, "44 cambio"],
  [fechaValida(29, 2, 2024) && !fechaValida(29, 2, 2026) && !fechaValida(31, 4, 2026), "45 fecha"],
  [diasHabilesEntre("2026-09-21", "2026-10-02") === 10 && diasHabilesEntre("2026-10-05", "2026-10-11", ["2026-10-09"]) === 4, "46 habiles"],
  [cuotaPrestamo(5000, 0.12, 12) === 444.24, "47 prestamo"],
  [primerNoRepetido("aabbcdc") === "d" && primerNoRepetido("aa") === null, "48 no repetido"],
  [igual(reordenInventario([{ codigo: "A", stock: 10, venta_diaria: 2 }, { codigo: "B", stock: 100, venta_diaria: 1 }]), [["A", 50]]), "49 reorden"],
  [igual(sistemaNotas([8, 7, 9], 6, 90), [7.2, "Aprobado"]) && sistemaNotas([5, 6], 5, 80)[1] === "Supletorio", "50 notas"],
];
casos.forEach(([ok, n]) => console.log((ok ? "OK    " : "FALLO ") + n));
console.log(`\n${casos.filter(([ok]) => ok).length}/${casos.length} correctas`);
