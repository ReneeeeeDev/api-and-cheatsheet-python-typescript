// Repaso de TypeScript: tipos, interfaces, types, uniones, genéricos, clases, enums, utilidades.
// Ejecutar sin configurar nada:   npx tsx basicos.ts        (descarga tsx la primera vez)
// O compilando:                   npm i -D typescript  →  npx tsc basicos.ts  →  node basicos.js
// Node 23.6+ ejecuta .ts directo:  node basicos.ts   (solo si no usas enum)

// ---------------------------------------------------------------- TIPOS BÁSICOS
let nombre: string = "Ana";
let edad: number = 25;
let activo: boolean = true;
let notas: number[] = [9, 8.5];
let tupla: [string, number] = ["Ana", 9];
let cualquiera: unknown = "usar unknown en vez de any";   // unknown obliga a verificar antes de usar
const inferido = 42;                                       // TS infiere number (literal 42)
console.log(nombre, edad, activo, notas, tupla, typeof cualquiera === "string" ? cualquiera.toUpperCase() : "");

// ---------------------------------------------------------------- INTERFACES Y TYPES
interface Producto {
  readonly id: number;          // no se puede modificar
  nombre: string;
  precio: number;
  stock?: number;               // opcional
  categoria: Categoria;
}

type Categoria = "perifericos" | "pantallas" | "redes";    // unión de literales
type ID = number | string;                                 // unión de tipos

interface ProductoDigital extends Producto {                // herencia de interfaces
  urlDescarga: string;
}

const mouse: Producto = { id: 1, nombre: "Mouse", precio: 15.5, categoria: "perifericos" };
// mouse.id = 2;              → error de compilación (readonly)
// mouse.categoria = "sillas" → error: no está en la unión

// ---------------------------------------------------------------- FUNCIONES TIPADAS
function calcularTotal(items: Producto[], iva: number = 0.15): number {
  return items.reduce((s, p) => s + p.precio * (p.stock ?? 1), 0) * (1 + iva);
}
const formatear = (valor: number, moneda: "USD" | "EUR" = "USD"): string => `${valor.toFixed(2)} ${moneda}`;
function buscar(id: ID): string {
  return typeof id === "number" ? `por número ${id}` : `por código ${id.toUpperCase()}`;   // narrowing
}
console.log(formatear(calcularTotal([mouse, { ...mouse, id: 2, precio: 10, stock: 3 }])), buscar(5), buscar("p01"));

// ---------------------------------------------------------------- GENÉRICOS
function primero<T>(lista: T[]): T | undefined {
  return lista[0];
}
interface RespuestaApi<T> {
  ok: boolean;
  datos: T;
  error?: string;
}
const resp: RespuestaApi<Producto[]> = { ok: true, datos: [mouse] };
console.log(primero([10, 20]), primero(["a"]), resp.datos.length);

class Repositorio<T extends { id: number }> {
  private items: T[] = [];
  crear(item: T): T { this.items.push(item); return item; }
  obtener(id: number): T | undefined { return this.items.find((i) => i.id === id); }
  actualizar(id: number, cambios: Partial<T>): T | undefined {
    const i = this.items.findIndex((x) => x.id === id);
    if (i === -1) return undefined;
    this.items[i] = { ...this.items[i], ...cambios };
    return this.items[i];
  }
  eliminar(id: number): boolean {
    const antes = this.items.length;
    this.items = this.items.filter((x) => x.id !== id);
    return this.items.length < antes;
  }
  listar(): readonly T[] { return this.items; }
}
const repo = new Repositorio<Producto>();
repo.crear(mouse);
repo.actualizar(1, { precio: 12 });
console.log(repo.listar(), repo.eliminar(99));

// ---------------------------------------------------------------- CLASES
abstract class Empleado {
  private static contador = 0;
  public readonly id: number;
  constructor(protected nombre: string) {       // "parameter properties": declara y asigna
    this.id = ++Empleado.contador;
  }
  abstract calcularSueldo(): number;
  describir(): string { return `#${this.id} ${this.nombre}: $${this.calcularSueldo().toFixed(2)}`; }
}
class Docente extends Empleado {
  constructor(nombre: string, private base: number, private materias: string[]) { super(nombre); }
  calcularSueldo(): number { return this.base + 25 * this.materias.length; }
}
console.log(new Docente("María", 1100, ["POO", "BD"]).describir());

// ---------------------------------------------------------------- ENUM
enum Estado { Pendiente = "PENDIENTE", EnProceso = "EN_PROCESO", Cerrado = "CERRADO" }
interface Ticket { id: number; titulo: string; estado: Estado; }
const t: Ticket = { id: 1, titulo: "Impresora", estado: Estado.Pendiente };
console.log(t.estado, Object.values(Estado));

// ---------------------------------------------------------------- UTILIDADES DE TIPOS
type ProductoNuevo = Omit<Producto, "id">;                 // todo menos id (para crear)
type ProductoEdicion = Partial<ProductoNuevo>;              // todo opcional (para PATCH)
type SoloNombrePrecio = Pick<Producto, "nombre" | "precio">;
type StockPorCategoria = Record<Categoria, number>;
const stock: StockPorCategoria = { perifericos: 20, pantallas: 3, redes: 0 };
const edicion: ProductoEdicion = { precio: 9.99 };
const np: SoloNombrePrecio = { nombre: "Cable", precio: 3 };
console.log(stock, edicion, np);

// ---------------------------------------------------------------- TIPAR FETCH
async function cargarUsuarios(): Promise<{ id: number; name: string }[]> {
  const r = await fetch("https://jsonplaceholder.typicode.com/users");
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return (await r.json()) as { id: number; name: string }[];
}
cargarUsuarios().then((u) => console.log("usuarios:", u.length)).catch((e: Error) => console.log("sin red:", e.message));

// ---------------------------------------------------------------- REACT CON TYPESCRIPT (referencia)
// interface Props { titulo: string; onGuardar: (p: Producto) => void; }
// function Formulario({ titulo, onGuardar }: Props) {
//   const [form, setForm] = useState<ProductoNuevo>({ nombre: "", precio: 0, categoria: "perifericos" });
//   const cambiar = (e: React.ChangeEvent<HTMLInputElement>) => setForm({ ...form, [e.target.name]: e.target.value });
//   ...
// }
