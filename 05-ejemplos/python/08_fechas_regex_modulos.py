"""08 - Fechas (datetime), expresiones regulares (re), random, math y módulos propios.
Ejecutar:  python 08_fechas_regex_modulos.py
"""
import math
import random
import re
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------- FECHAS
hoy = date.today()
ahora = datetime.now()
print(hoy, ahora.strftime("%d/%m/%Y %H:%M"))                  # 2026-09-25 25/09/2026 12:30

nacimiento = date(2001, 3, 15)
edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
print("Edad:", edad)

vence = hoy + timedelta(days=30)
print("Vence:", vence, "| faltan", (vence - hoy).days, "días")

f = datetime.strptime("25/09/2026 16:00", "%d/%m/%Y %H:%M")   # texto → fecha
print(f, f.weekday(), f.strftime("%A"), f.isoformat())         # weekday: 0 = lunes

inicio, fin = datetime.strptime("08:00", "%H:%M"), datetime.strptime("10:30", "%H:%M")
print("Duración en horas:", (fin - inicio).total_seconds() / 3600)   # 2.5

# Códigos de formato: %d día, %m mes, %Y año 4 dígitos, %H hora 24h, %M minutos, %S segundos
# Formato ISO (el que usan las BD y los <input type="date">): AAAA-MM-DD → date.fromisoformat("2026-09-25")
print(date.fromisoformat("2026-09-25") > date(2026, 1, 1))

# Días hábiles entre dos fechas
def dias_habiles(desde, hasta):
    return sum(1 for i in range((hasta - desde).days + 1) if (desde + timedelta(i)).weekday() < 5)
print("Días hábiles de septiembre 2026:", dias_habiles(date(2026, 9, 1), date(2026, 9, 30)))

# ---------------------------------------------------------------- EXPRESIONES REGULARES
patrones = {
    "email":     r"^[\w.+-]+@[\w-]+\.[\w.-]+$",
    "celular":   r"^09\d{8}$",                        # Ecuador: 09 + 8 dígitos
    "cedula":    r"^\d{10}$",
    "placa":     r"^[A-Z]{3}-\d{3,4}$",               # ABC-1234
    "hora":      r"^([01]\d|2[0-3]):[0-5]\d$",
    "password":  r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$",   # min 8, mayúscula, minúscula, dígito
}
pruebas = {
    "email": ["ana@mail.com", "ana@@mail"], "celular": ["0987654321", "0887654321"],
    "cedula": ["1710034065", "17100"], "placa": ["TBA-1234", "tba1234"],
    "hora": ["23:59", "24:00"], "password": ["Clave123", "clave123"],
}
for nombre, patron in patrones.items():
    print(f"{nombre:<9}", [(v, bool(re.match(patron, v))) for v in pruebas[nombre]])

texto = "Llamar al 0987654321 o al 0991112233. Correo: soporte@iste.edu.ec"
print(re.findall(r"09\d{8}", texto))                           # ['0987654321', '0991112233']
print(re.search(r"[\w.]+@[\w.]+", texto).group())              # soporte@iste.edu.ec
print(re.sub(r"\d{6}(\d{4})", r"******\1", texto))             # ocultar dígitos
print(re.split(r"[,;\s]+", "a, b;c  d"))                       # ['a', 'b', 'c', 'd']
m = re.match(r"(\d{4})-(\d{2})-(\d{2})", "2026-09-25")
print(m.groups(), m.group(1))                                  # ('2026', '09', '25') 2026

# ---------------------------------------------------------------- RANDOM Y MATH
random.seed(1)                                                 # resultados repetibles
print(random.randint(1, 6), random.choice(["a", "b", "c"]), random.sample(range(10), 3))
lista = [1, 2, 3, 4]; random.shuffle(lista); print(lista)
print(math.sqrt(16), math.pi, math.ceil(4.1), math.floor(4.9), math.gcd(12, 18), math.factorial(5))
print(math.isclose(0.1 + 0.2, 0.3), math.hypot(3, 4))

# Dinero: usa Decimal para evitar errores de redondeo
from decimal import Decimal, ROUND_HALF_UP
total = Decimal("0.1") + Decimal("0.2")
print(total, total == Decimal("0.3"))                          # 0.3 True
iva = (Decimal("19.99") * Decimal("0.15")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print("IVA 15%:", iva)                                         # 3.00

# ---------------------------------------------------------------- MÓDULOS PROPIOS
# Si creas utilidades.py con:   def sumar(a, b): return a + b
# desde otro archivo en la MISMA carpeta:
#     from utilidades import sumar          o      import utilidades as u
# if __name__ == "__main__":  → código que solo corre al ejecutar el archivo directamente,
#                               no al importarlo.
print("__name__ de este archivo:", __name__)
