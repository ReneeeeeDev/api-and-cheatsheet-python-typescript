// 08 - Fechas (Date e Intl) y expresiones regulares.
// Ejecutar:  node 08_fechas_regex.js

// ---------------------------------------------------------------- FECHAS
const ahora = new Date();
console.log(ahora.toISOString());                               // 2026-09-25T17:30:00.000Z (UTC)
console.log(ahora.toLocaleDateString("es-EC"), ahora.toLocaleTimeString("es-EC", { hour: "2-digit", minute: "2-digit" }));
console.log(new Intl.DateTimeFormat("es-EC", { dateStyle: "full" }).format(ahora));

// ¡OJO! Los meses van de 0 a 11
const f = new Date(2026, 8, 25, 16, 0);                         // 25 de septiembre de 2026, 16:00 (hora local)
console.log(f.getFullYear(), f.getMonth() + 1, f.getDate(), f.getDay(), f.getHours());   // getDay: 0=domingo

// "AAAA-MM-DD" (lo que envía <input type="date">) se interpreta como UTC → puede mostrar el día anterior en Ecuador.
const desdeInput = "2026-09-25";
const [anio, mes, dia] = desdeInput.split("-").map(Number);
const local = new Date(anio, mes - 1, dia);                     // forma segura
console.log(local.toLocaleDateString("es-EC"));

// Sumar días y diferencia
const en30 = new Date(local); en30.setDate(en30.getDate() + 30);
const diasEntre = Math.round((en30 - local) / 86_400_000);       // restar fechas da milisegundos
console.log(en30.toLocaleDateString("es-EC"), diasEntre);

// Formatear AAAA-MM-DD a mano
const aISO = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
console.log(aISO(local));

// Edad
function calcularEdad(nacimientoISO) {
  const [a, m, d] = nacimientoISO.split("-").map(Number);
  const hoy = new Date();
  let edad = hoy.getFullYear() - a;
  if (hoy.getMonth() + 1 < m || (hoy.getMonth() + 1 === m && hoy.getDate() < d)) edad--;
  return edad;
}
console.log("edad:", calcularEdad("2001-03-15"));

// Horas "HH:MM" → minutos (para calcular duraciones o choques)
const aMinutos = (h) => { const [hh, mm] = h.split(":").map(Number); return hh * 60 + mm; };
console.log("duración:", (aMinutos("10:30") - aMinutos("08:00")) / 60, "horas");

// Números y moneda
console.log(new Intl.NumberFormat("es-EC", { style: "currency", currency: "USD" }).format(1234.5));
console.log(new Intl.NumberFormat("es-EC", { style: "percent" }).format(0.256));

// ---------------------------------------------------------------- EXPRESIONES REGULARES
const patrones = {
  email: /^[\w.+-]+@[\w-]+\.[\w.-]+$/,
  celular: /^09\d{8}$/,
  cedula: /^\d{10}$/,
  placa: /^[A-Z]{3}-\d{3,4}$/,
  hora: /^([01]\d|2[0-3]):[0-5]\d$/,
  password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/,
};
const pruebas = {
  email: ["ana@mail.com", "ana@@mail"], celular: ["0987654321", "0887654321"], cedula: ["1710034065", "17100"],
  placa: ["TBA-1234", "tba1234"], hora: ["23:59", "24:00"], password: ["Clave123", "clave123"],
};
for (const [n, re] of Object.entries(patrones)) console.log(n.padEnd(9), pruebas[n].map((v) => `${v}:${re.test(v)}`).join("  "));

const texto = "Llamar al 0987654321 o al 0991112233. Correo: soporte@iste.edu.ec";
console.log(texto.match(/09\d{8}/g));                               // todas las coincidencias
console.log(texto.match(/[\w.]+@[\w.]+/)[0]);
console.log(texto.replace(/\d{6}(\d{4})/g, "******$1"));            // grupos con $1
const m = "2026-09-25".match(/(?<a>\d{4})-(?<m>\d{2})-(?<d>\d{2})/);
console.log(m.groups.a, m.groups.m, m.groups.d);                    // grupos con nombre
console.log("a, b;c  d".split(/[,;\s]+/));
for (const coincidencia of texto.matchAll(/09(\d{8})/g)) console.log("resto:", coincidencia[1]);
// Banderas: g (todas), i (ignorar mayúsculas), m (multilínea), u (unicode)
