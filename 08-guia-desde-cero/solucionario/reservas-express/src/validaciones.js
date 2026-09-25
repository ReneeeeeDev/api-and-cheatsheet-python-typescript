// Reglas de negocio. Cada función recibe la conexión (db) y los datos del formulario
// y devuelve un arreglo de mensajes de error (arreglo vacío = todo correcto).

export const ESTADOS = ["disponible", "mantenimiento"];
const PATRON_HORA = /^([01]\d|2[0-3]):[0-5]\d$/;     // 00:00 a 23:59
const PATRON_FECHA = /^\d{4}-\d{2}-\d{2}$/;          // 2026-09-25

// Dos horarios [ini, fin) se cruzan si uno empieza antes de que termine el otro.
// Las horas "HH:MM" se pueden comparar como texto.
export const seCruzan = (ini1, fin1, ini2, fin2) => ini1 < fin2 && ini2 < fin1;

const esEntero = (valor, minimo) => /^\d+$/.test(String(valor ?? "").trim()) && Number(valor) >= minimo;

export function validarLaboratorio(db, datos, idActual = 0) {
  const errores = [];
  const codigo = String(datos.codigo ?? "").trim().toUpperCase();
  const nombre = String(datos.nombre ?? "").trim();

  if (!codigo) {
    errores.push("El código es obligatorio.");
  } else if (db.prepare("SELECT 1 FROM laboratorios WHERE codigo = ? AND id <> ?").get(codigo, idActual)) {
    errores.push(`Ya existe un laboratorio con el código ${codigo}.`);
  }
  if (nombre.length < 3) errores.push("El nombre debe tener al menos 3 caracteres.");
  if (!esEntero(datos.piso, 0)) errores.push("El piso debe ser un número entero (0 o mayor).");
  if (!esEntero(datos.capacidad, 1)) errores.push("La capacidad debe ser un número entero mayor a 0.");
  if (!ESTADOS.includes(datos.estado ?? "disponible"))
    errores.push("El estado debe ser 'disponible' o 'mantenimiento'.");
  return errores;
}

// Devuelve la reserva que se cruza con el horario pedido, o undefined.
export function buscarChoque(db, laboratorioId, fecha, horaInicio, horaFin) {
  return db.prepare(
    `SELECT * FROM reservas
     WHERE laboratorio_id = ? AND fecha = ?
       AND hora_inicio < ? AND ? < hora_fin`
  ).get(laboratorioId, fecha, horaFin, horaInicio);
}

export function validarReserva(db, datos) {
  const errores = [];
  const docente = String(datos.docente ?? "").trim();
  const fecha = String(datos.fecha ?? "");
  const inicio = String(datos.hora_inicio ?? "");
  const fin = String(datos.hora_fin ?? "");
  const lab = db.prepare("SELECT * FROM laboratorios WHERE id = ?").get(Number(datos.laboratorio_id) || 0);

  if (docente.length < 3) errores.push("El nombre del docente es obligatorio (mínimo 3 caracteres).");
  if (!lab) errores.push("Seleccione un laboratorio válido.");
  else if (lab.estado === "mantenimiento")
    errores.push(`${lab.nombre} está en mantenimiento y no se puede reservar.`);
  if (!PATRON_FECHA.test(fecha)) errores.push("La fecha es obligatoria.");
  if (!PATRON_HORA.test(inicio) || !PATRON_HORA.test(fin))
    errores.push("Las horas de inicio y fin son obligatorias (HH:MM).");
  else if (fin <= inicio) errores.push("La hora de fin debe ser mayor que la hora de inicio.");

  // Solo buscamos choques si lo anterior está bien
  if (errores.length === 0) {
    const choque = buscarChoque(db, lab.id, fecha, inicio, fin);
    if (choque)
      errores.push(`Horario ocupado: ${choque.hora_inicio}-${choque.hora_fin} reservado por ${choque.docente}.`);
  }
  return errores;
}
