"""05 - Programación Orientada a Objetos: clases, encapsulamiento, herencia, polimorfismo,
abstracción, métodos de clase/estáticos, propiedades, métodos especiales y dataclasses.
Ejecutar:  python 05_poo.py
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------- CLASE BÁSICA + ENCAPSULAMIENTO
class CuentaBancaria:
    banco = "Banco ISTE"                 # atributo de CLASE (compartido)
    _contador = 0

    def __init__(self, titular, saldo_inicial=0.0):
        CuentaBancaria._contador += 1
        self.numero = f"CTA-{CuentaBancaria._contador:04d}"
        self.titular = titular           # atributo de INSTANCIA (público)
        self.__saldo = 0.0               # "privado": name mangling → _CuentaBancaria__saldo
        self.movimientos = []
        if saldo_inicial:
            self.depositar(saldo_inicial)

    @property                            # getter: se usa como atributo cuenta.saldo
    def saldo(self):
        return self.__saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("Monto inválido")
        self.__saldo += monto
        self.movimientos.append(("+", monto))

    def retirar(self, monto):
        if monto > self.__saldo:
            raise ValueError("Saldo insuficiente")
        self.__saldo -= monto
        self.movimientos.append(("-", monto))

    @classmethod                          # recibe la clase: constructor alternativo
    def desde_texto(cls, texto):
        titular, saldo = texto.split(";")
        return cls(titular, float(saldo))

    @staticmethod                         # no usa self ni cls: utilidad
    def es_monto_valido(monto):
        return isinstance(monto, (int, float)) and monto > 0

    def __str__(self):                    # print(obj)
        return f"{self.numero} - {self.titular}: ${self.__saldo:.2f}"

    def __repr__(self):                   # en listas / consola
        return f"CuentaBancaria({self.titular!r}, {self.__saldo})"


c1 = CuentaBancaria("Ana", 100)
c1.depositar(50)
c1.retirar(30)
c2 = CuentaBancaria.desde_texto("Luis;500")
print(c1, "|", c2, "|", CuentaBancaria.banco)
print(c1.saldo, CuentaBancaria.es_monto_valido(-3), [c1, c2])
# c1.saldo = 999   → AttributeError: no tiene setter
# c1.__saldo       → AttributeError (está "oculto")


# ---------------------------------------------------------------- PROPERTY CON SETTER (validación)
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio             # pasa por el setter

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = round(valor, 2)

p = Producto("Mouse", 12.456)
print(p.precio)                           # 12.46
try:
    p.precio = -1
except ValueError as e:
    print("Error:", e)


# ---------------------------------------------------------------- HERENCIA, ABSTRACCIÓN, POLIMORFISMO
class Empleado(ABC):                      # clase abstracta: no se puede instanciar
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    @abstractmethod
    def calcular_sueldo(self):
        """Cada tipo de empleado lo calcula distinto."""

    def aporte_iess(self):
        return round(self.calcular_sueldo() * 0.0945, 2)

    def __str__(self):
        return f"{type(self).__name__:<12} {self.nombre:<8} sueldo ${self.calcular_sueldo():>8.2f} IESS ${self.aporte_iess():>7.2f}"


class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, cedula, sueldo_base):
        super().__init__(nombre, cedula)  # llama al constructor del padre
        self.sueldo_base = sueldo_base

    def calcular_sueldo(self):
        return self.sueldo_base


class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, cedula, horas, tarifa):
        super().__init__(nombre, cedula)
        self.horas, self.tarifa = horas, tarifa

    def calcular_sueldo(self):
        extra = max(0, self.horas - 160) * self.tarifa * 0.5     # horas extra al 150 %
        return self.horas * self.tarifa + extra


class Docente(EmpleadoTiempoCompleto):
    def __init__(self, nombre, cedula, sueldo_base, materias):
        super().__init__(nombre, cedula, sueldo_base)
        self.materias = materias

    def calcular_sueldo(self):                                   # sobrescritura
        return super().calcular_sueldo() + 25 * len(self.materias)


nomina = [
    EmpleadoTiempoCompleto("Ana", "1710034065", 900),
    EmpleadoPorHoras("Luis", "0926687856", 170, 5),
    Docente("María", "1804432126", 1100, ["POO", "BD", "Web"]),
]
for e in nomina:                          # POLIMORFISMO: misma llamada, distinto comportamiento
    print(e)
print("Total nómina:", sum(e.calcular_sueldo() for e in nomina))
print(isinstance(nomina[2], Empleado), issubclass(Docente, EmpleadoTiempoCompleto))  # True True
try:
    Empleado("X", "1")
except TypeError as e:
    print("No se puede instanciar clase abstracta:", type(e).__name__)


# ---------------------------------------------------------------- COMPOSICIÓN ("tiene un")
class Carrito:
    def __init__(self):
        self.items = []                    # un carrito TIENE productos

    def agregar(self, producto, cantidad=1):
        self.items.append((producto, cantidad))
        return self                        # permite encadenar

    def total(self):
        return round(sum(p.precio * c for p, c in self.items), 2)

    def __len__(self):
        return sum(c for _, c in self.items)

carrito = Carrito().agregar(Producto("Teclado", 25)).agregar(Producto("Mouse", 10), 3)
print("Artículos:", len(carrito), "Total:", carrito.total())


# ---------------------------------------------------------------- MÉTODOS ESPECIALES
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, otro):               # v1 + v2
        return Vector(self.x + otro.x, self.y + otro.y)
    def __eq__(self, otro):                # v1 == v2
        return (self.x, self.y) == (otro.x, otro.y)
    def __lt__(self, otro):                # permite sorted()
        return (self.x ** 2 + self.y ** 2) < (otro.x ** 2 + otro.y ** 2)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4), Vector(1, 1) == Vector(1, 1), sorted([Vector(3, 3), Vector(1, 0)]))


# ---------------------------------------------------------------- DATACLASS (menos código)
@dataclass
class Estudiante:
    nombre: str
    cedula: str
    notas: list = field(default_factory=list)

    @property
    def promedio(self):
        return round(sum(self.notas) / len(self.notas), 2) if self.notas else 0

@dataclass(frozen=True, order=True)       # inmutable y ordenable
class Hora:
    h: int
    m: int

e = Estudiante("Ana", "1710034065", [9, 8.5, 10])
print(e, e.promedio)
print(Hora(8, 0) < Hora(9, 30), sorted([Hora(14, 0), Hora(8, 15)]))
