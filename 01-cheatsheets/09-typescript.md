# Cheatsheet TypeScript

> Ejemplo ejecutable: `05-ejemplos/typescript/basicos.ts` → `npx tsx basicos.ts`

## 1. Qué es y cómo se ejecuta

TypeScript = JavaScript + **tipos estáticos**. El navegador y Node no entienden los tipos, así que se **compila** a JS (`tsc`) o se ejecuta con una herramienta que quita los tipos (`tsx`, Vite, Next).

```bash
npm init -y
npm i -D typescript tsx @types/node
npx tsc --init                      # crea tsconfig.json
npx tsx archivo.ts                  # ejecutar directamente (desarrollo)
npx tsc                             # compilar todo el proyecto a JS (según tsconfig: outDir)
npx tsc --noEmit                    # solo verificar tipos, sin generar archivos
node dist/archivo.js
```
React + TS: `npm create vite@latest app -- --template react-ts`. Next ya trae TS.

`tsconfig.json` mínimo:
```json
{ "compilerOptions": { "target": "ES2022", "module": "NodeNext", "strict": true, "outDir": "dist", "esModuleInterop": true, "skipLibCheck": true }, "include": ["src"] }
```

## 2. Tipos

```ts
let n: number = 5; let s: string = "a"; let b: boolean = true;
let lista: number[] = [1, 2]; let otra: Array<string> = ["a"];
let tupla: [string, number] = ["Ana", 9];
let u: string | null = null;               // unión
let lit: "GET" | "POST" = "GET";           // literales
let x: unknown;                            // seguro: obliga a comprobar el tipo
let y: any;                                // desactiva el chequeo (evítalo)
function f(): void {}                      // no devuelve nada
function error(): never { throw new Error(); }
const config = { puerto: 3000 } as const; // readonly literal
```

## 3. Interfaces y type

```ts
interface Usuario {
  readonly id: number;
  nombre: string;
  email?: string;                          // opcional
  roles: Rol[];
  [clave: string]: unknown;                // propiedades extra (index signature)
}
type Rol = "admin" | "docente" | "estudiante";
type Punto = { x: number; y: number };
type ConId = Usuario & { creadoEn: Date }; // intersección
interface Admin extends Usuario { permisos: string[] }
```
¿`interface` o `type`? Usa `interface` para objetos que se extienden y `type` para uniones, intersecciones y alias.

## 4. Funciones

```ts
function sumar(a: number, b = 0): number { return a + b; }
const mult = (a: number, b: number): number => a * b;
function saludar(nombre: string, saludo?: string) { }
function total(...nums: number[]) { }
type Callback = (error: Error | null, datos?: string) => void;
// Sobrecarga
function formato(x: number): string;
function formato(x: Date): string;
function formato(x: number | Date) { return String(x); }
```

## 5. Narrowing (reducir tipos)

```ts
function procesar(v: string | number | null) {
  if (v === null) return;
  if (typeof v === "string") return v.toUpperCase();    // aquí v es string
  return v.toFixed(2);                                  // aquí v es number
}
if (err instanceof Error) err.message;
if ("email" in usuario) usuario.email;
// Unión discriminada (muy útil)
type Resultado = { ok: true; datos: string[] } | { ok: false; error: string };
function mostrar(r: Resultado) { r.ok ? r.datos.length : r.error; }
// Type guard propio
const esUsuario = (o: any): o is Usuario => typeof o?.id === "number";
```

## 6. Genéricos

```ts
function primero<T>(arr: T[]): T | undefined { return arr[0]; }
interface Respuesta<T> { datos: T; total: number; }
class Pila<T> { private items: T[] = []; push(x: T) { this.items.push(x); } pop(): T | undefined { return this.items.pop(); } }
function obtener<T extends { id: number }>(lista: T[], id: number): T | undefined { return lista.find((x) => x.id === id); }
async function api<T>(url: string): Promise<T> { const r = await fetch(url); return r.json() as Promise<T>; }
const usuarios = await api<Usuario[]>("/api/usuarios");
```

## 7. Tipos utilitarios

| Tipo | Resultado |
|---|---|
| `Partial<T>` | todas las propiedades opcionales (para PATCH) |
| `Required<T>` | todas obligatorias |
| `Readonly<T>` | todas de solo lectura |
| `Pick<T, "a" \| "b">` | solo esas propiedades |
| `Omit<T, "id">` | todas menos esas (para crear) |
| `Record<K, V>` | objeto con claves K y valores V |
| `ReturnType<typeof f>` | tipo que devuelve la función |
| `Awaited<Promise<T>>` | T |
| `NonNullable<T>` | quita null/undefined |
| `keyof T` | unión de las claves |
| `typeof variable` | tipo de una variable |

## 8. Clases

```ts
abstract class Figura {
  constructor(protected readonly nombre: string) {}
  abstract area(): number;
  describir() { return `${this.nombre}: ${this.area().toFixed(2)}`; }
}
class Circulo extends Figura implements Comparable {
  static readonly PI = Math.PI;
  #privadoReal = 1;                            // privado en tiempo de ejecución
  constructor(private radio: number) { super("Círculo"); }
  area() { return Circulo.PI * this.radio ** 2; }
  comparar(o: Circulo) { return this.area() - o.area(); }
}
interface Comparable { comparar(o: any): number; }
```

## 9. Enums

```ts
enum Estado { Abierto = "ABIERTO", Cerrado = "CERRADO" }
// Alternativa moderna (sin enum): objeto + as const
const ESTADOS = { Abierto: "ABIERTO", Cerrado: "CERRADO" } as const;
type EstadoT = typeof ESTADOS[keyof typeof ESTADOS];      // "ABIERTO" | "CERRADO"
```

## 10. TypeScript con Express y con React

```ts
import express, { Request, Response, NextFunction } from "express";   // npm i -D @types/express
interface Producto { id: number; nombre: string; precio: number }
const app = express();
app.use(express.json());
app.get("/api/productos/:id", (req: Request<{ id: string }>, res: Response<Producto | { error: string }>) => {
  const p = productos.find((x) => x.id === Number(req.params.id));
  if (!p) return res.status(404).json({ error: "No encontrado" });
  res.json(p);
});
```
```tsx
interface Props { producto: Producto; onEliminar: (id: number) => void; }
export function Fila({ producto, onEliminar }: Props) {
  const [editando, setEditando] = useState<boolean>(false);
  const [lista, setLista] = useState<Producto[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const cambiar = (e: React.ChangeEvent<HTMLInputElement>) => {};
  const enviar = (e: React.FormEvent<HTMLFormElement>) => { e.preventDefault(); };
  return <tr><td>{producto.nombre}</td><td><button onClick={() => onEliminar(producto.id)}>X</button></td></tr>;
}
```

## 11. Errores típicos del compilador

| Mensaje | Significado |
|---|---|
| `Type 'string' is not assignable to type 'number'` | Tipos incompatibles |
| `Object is possibly 'undefined'` | Usa `?.`, `??`, o comprueba antes (`if (x)`) |
| `Property 'x' does not exist on type 'Y'` | Falta en la interfaz, o hay un error al escribir el nombre |
| `Argument of type ... is not assignable to parameter` | Pasaste un tipo incorrecto |
| `Parameter 'x' implicitly has an 'any' type` | Con `strict` debes tipar el parámetro |
| `Cannot find module 'x' or its corresponding type declarations` | Instala `@types/x` |

**Preguntas típicas:** ¿Ventajas de TS? Detecta errores antes de ejecutar, da mejor autocompletado, facilita refactorizar y documenta el código. ¿`any` vs `unknown`? `any` apaga el chequeo; `unknown` obliga a verificar el tipo antes de usarlo.
