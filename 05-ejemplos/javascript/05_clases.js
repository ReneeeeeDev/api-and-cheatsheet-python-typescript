// 05 - POO en JavaScript: clases, campos privados, getters/setters, static, herencia, polimorfismo.
// Ejecutar:  node 05_clases.js

class CuentaBancaria {
  static #contador = 0;             // campo estático privado
  #saldo = 0;                       // campo privado REAL (no accesible desde fuera)

  constructor(titular, saldoInicial = 0) {
    this.numero = `CTA-${String(++CuentaBancaria.#contador).padStart(4, "0")}`;
    this.titular = titular;
    this.movimientos = [];
    if (saldoInicial > 0) this.depositar(saldoInicial);
  }

  get saldo() { return this.#saldo; }                    // getter: cuenta.saldo

  depositar(monto) {
    if (!CuentaBancaria.esMontoValido(monto)) throw new Error("Monto inválido");
    this.#saldo += monto;
    this.movimientos.push({ tipo: "+", monto });
    return this;                                         // permite encadenar
  }

  retirar(monto) {
    if (monto > this.#saldo) throw new Error("Saldo insuficiente");
    this.#saldo -= monto;
    this.movimientos.push({ tipo: "-", monto });
    return this;
  }

  static esMontoValido(m) { return typeof m === "number" && m > 0; }

  toString() { return `${this.numero} ${this.titular}: $${this.#saldo.toFixed(2)}`; }
}

const cuenta = new CuentaBancaria("Ana", 100).depositar(50).retirar(30);
console.log(String(cuenta), cuenta.saldo, CuentaBancaria.esMontoValido(-1));
// console.log(cuenta.#saldo)  → SyntaxError
try { cuenta.retirar(1000); } catch (e) { console.log("Error:", e.message); }

// ---------------------------------------------------------------- SETTER CON VALIDACIÓN
class Producto {
  #precio;
  constructor(nombre, precio) { this.nombre = nombre; this.precio = precio; }
  get precio() { return this.#precio; }
  set precio(v) {
    if (v < 0) throw new RangeError("Precio negativo");
    this.#precio = Math.round(v * 100) / 100;
  }
}
const p = new Producto("Mouse", 12.456);
console.log(p.precio);                                   // 12.46

// ---------------------------------------------------------------- HERENCIA Y POLIMORFISMO
class Empleado {
  constructor(nombre) {
    if (new.target === Empleado) throw new TypeError("Empleado es abstracta");
    this.nombre = nombre;
  }
  calcularSueldo() { throw new Error("Implementar en la subclase"); }
  aporteIess() { return +(this.calcularSueldo() * 0.0945).toFixed(2); }
  describir() { return `${this.constructor.name.padEnd(10)} ${this.nombre.padEnd(6)} $${this.calcularSueldo().toFixed(2)}`; }
}

class TiempoCompleto extends Empleado {
  constructor(nombre, sueldo) { super(nombre); this.sueldo = sueldo; }
  calcularSueldo() { return this.sueldo; }
}

class PorHoras extends Empleado {
  constructor(nombre, horas, tarifa) { super(nombre); Object.assign(this, { horas, tarifa }); }
  calcularSueldo() { return this.horas * this.tarifa; }
}

class Docente extends TiempoCompleto {
  constructor(nombre, sueldo, materias) { super(nombre, sueldo); this.materias = materias; }
  calcularSueldo() { return super.calcularSueldo() + 25 * this.materias.length; }   // sobrescribe
}

const nomina = [new TiempoCompleto("Ana", 900), new PorHoras("Luis", 160, 5), new Docente("María", 1100, ["POO", "BD"])];
nomina.forEach((e) => console.log(e.describir(), "IESS:", e.aporteIess()));
console.log("Total:", nomina.reduce((s, e) => s + e.calcularSueldo(), 0));
console.log(nomina[2] instanceof Empleado, nomina[2] instanceof PorHoras);            // true false
try { new Empleado("X"); } catch (e) { console.log(e.message); }

// ---------------------------------------------------------------- "INTERFACES" CON MIXINS
const Serializable = (Base) => class extends Base {
  aJSON() { return JSON.stringify(this); }
};
class Alumno extends Serializable(Object) {
  constructor(nombre, notas) { super(); this.nombre = nombre; this.notas = notas; }
  get promedio() { return this.notas.reduce((s, n) => s + n, 0) / this.notas.length; }
}
const al = new Alumno("Ana", [9, 10]);
console.log(al.aJSON(), al.promedio);

// ---------------------------------------------------------------- CLASE REPOSITORIO (CRUD en memoria)
class Repositorio {
  #items = new Map();
  #nextId = 1;
  crear(datos) { const item = { id: this.#nextId++, ...datos }; this.#items.set(item.id, item); return item; }
  listar(filtro = () => true) { return [...this.#items.values()].filter(filtro); }
  obtener(id) { return this.#items.get(id) ?? null; }
  actualizar(id, cambios) {
    const actual = this.obtener(id);
    if (!actual) return null;
    const nuevo = { ...actual, ...cambios, id };
    this.#items.set(id, nuevo);
    return nuevo;
  }
  eliminar(id) { return this.#items.delete(id); }
}
const repo = new Repositorio();
repo.crear({ nombre: "Lab Redes", capacidad: 25 });
repo.crear({ nombre: "Lab Software", capacidad: 30 });
repo.actualizar(1, { capacidad: 28 });
repo.eliminar(2);
console.log(repo.listar(), repo.obtener(99), repo.eliminar(99));
