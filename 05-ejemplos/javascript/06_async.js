// 06 - Asincronía: event loop, callbacks, promesas, async/await, fetch, Promise.all, timeouts.
// Ejecutar:  node 06_async.js   (la parte de fetch necesita internet; si no hay, muestra el error)

// ---------------------------------------------------------------- ORDEN DE EJECUCIÓN (event loop)
console.log("1. síncrono");
setTimeout(() => console.log("4. setTimeout (macrotarea)"), 0);
Promise.resolve().then(() => console.log("3. promesa (microtarea)"));
console.log("2. síncrono");
// Primero todo lo síncrono, luego microtareas (promesas), luego macrotareas (timers).

// ---------------------------------------------------------------- CREAR UNA PROMESA
const esperar = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function obtenerUsuario(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id <= 0) reject(new Error("ID inválido"));
      else resolve({ id, nombre: `Usuario ${id}` });
    }, 50);
  });
}

// ---------------------------------------------------------------- .then / .catch
obtenerUsuario(1)
  .then((u) => { console.log("then:", u.nombre); return obtenerUsuario(-1); })
  .then(() => console.log("no llega aquí"))
  .catch((e) => console.log("catch:", e.message))
  .finally(() => console.log("finally de la cadena"));

// ---------------------------------------------------------------- ASYNC / AWAIT (lo más usado)
async function principal() {
  await esperar(200);
  console.log("\n--- async/await");

  try {
    const u = await obtenerUsuario(2);
    console.log("await:", u);
    await obtenerUsuario(0);
  } catch (e) {
    console.log("error capturado:", e.message);
  }

  // Secuencial vs paralelo
  let t = Date.now();
  await obtenerUsuario(1); await obtenerUsuario(2); await obtenerUsuario(3);
  console.log(`secuencial: ~${Date.now() - t} ms`);

  t = Date.now();
  const varios = await Promise.all([obtenerUsuario(1), obtenerUsuario(2), obtenerUsuario(3)]);
  console.log(`paralelo:   ~${Date.now() - t} ms`, varios.map((u) => u.id));

  // allSettled: no falla si una falla
  const resultados = await Promise.allSettled([obtenerUsuario(1), obtenerUsuario(-5)]);
  console.log(resultados.map((r) => r.status));             // ['fulfilled', 'rejected']

  // race: timeout
  const conTimeout = (promesa, ms) =>
    Promise.race([promesa, new Promise((_, rej) => setTimeout(() => rej(new Error("Tiempo agotado")), ms))]);
  try { await conTimeout(esperar(500), 100); } catch (e) { console.log("race:", e.message); }

  // Bucle con await (en serie)
  for (const id of [4, 5]) console.log("for await:", (await obtenerUsuario(id)).nombre);
  // ¡OJO! forEach NO espera a los await. Usa for...of o Promise.all con map.

  // ---------------------------------------------------------------- FETCH (Node 18+ y navegador)
  console.log("\n--- fetch a una API pública");
  try {
    const res = await fetch("https://jsonplaceholder.typicode.com/users?_limit=3", { signal: AbortSignal.timeout(4000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);        // fetch NO lanza error con 404/500
    const usuarios = await res.json();
    console.log(usuarios.map((u) => `${u.id} ${u.name} (${u.address.city})`));

    const nuevo = await fetch("https://jsonplaceholder.typicode.com/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "Prueba", body: "Hola", userId: 1 }),
      signal: AbortSignal.timeout(4000),
    });
    console.log("POST status:", nuevo.status, await nuevo.json());
  } catch (e) {
    console.log("Sin conexión o error de red:", e.name, e.message);
  }

  // Patrón típico en frontend:
  // async function cargar() {
  //   setCargando(true);
  //   try { const r = await fetch(url); if (!r.ok) throw new Error(r.status); setDatos(await r.json()); }
  //   catch (e) { setError(e.message); }
  //   finally { setCargando(false); }
  // }

  // setInterval
  let ticks = 0;
  const id = setInterval(() => {
    ticks++;
    if (ticks === 3) { clearInterval(id); console.log("\nintervalo detenido tras 3 ticks"); }
  }, 20);
}

principal();
