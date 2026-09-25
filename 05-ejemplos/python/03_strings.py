"""03 - Cadenas de texto: métodos, slicing, validaciones y ejercicios típicos.
Ejecutar:  python 03_strings.py
"""
import string
import unicodedata

s = "  Hola Mundo Python  "
print(repr(s.strip()), repr(s.lstrip()), repr(s.rstrip()))
print(s.lower(), s.upper(), s.title(), s.strip().swapcase())
print(s.replace("o", "0"), s.count("o"), s.find("Mundo"), s.find("xyz"))   # find da -1 si no existe
print(s.split(), "Hola,Mundo,,X".split(","))       # ['Hola', 'Mundo', 'Python'] ['Hola', 'Mundo', '', 'X']
print("-".join(["2026", "09", "25"]))              # 2026-09-25
print("Mundo" in s, s.strip().startswith("Hola"), s.strip().endswith("on"))

# Slicing
t = "Programación"
print(t[0], t[-1], t[0:4], t[4:], t[::-1], t[::2])  # P n Prog ramación nóicamargorP Pormcó

# Validaciones
print("123".isdigit(), "abc".isalpha(), "abc123".isalnum(), "  ".isspace(), "Hola".istitle())
print("hola mundo".capitalize(), "7".zfill(3), "Ana".center(9, "*"), "Ana".ljust(6, ".") + "|")

# Recorrer y caracteres
for i, c in enumerate("abc"):
    print(i, c, ord(c), chr(ord(c) + 1))         # código ASCII / Unicode
print(string.ascii_lowercase, string.digits, string.punctuation[:10])

# Quitar tildes
def quitar_tildes(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")
print(quitar_tildes("Árbol, canción, pingüino, ñandú"))   # Arbol, cancion, pinguino, nandu

# Los strings son INMUTABLES: s[0] = "X" da error. Se construye uno nuevo:
palabra = "gato"
print("p" + palabra[1:])                           # pato

# ------------------------------------------------------------ EJERCICIOS TÍPICOS
def es_palindromo(texto):
    limpio = [c for c in quitar_tildes(texto.lower()) if c.isalnum()]
    return limpio == limpio[::-1]

def contar_vocales(texto):
    return sum(1 for c in quitar_tildes(texto.lower()) if c in "aeiou")

def capitalizar_palabras(texto):
    return " ".join(p[:1].upper() + p[1:].lower() for p in texto.split())

def palabra_mas_larga(texto):
    return max(texto.split(), key=len)

def iniciales(nombre_completo):
    return "".join(p[0].upper() + "." for p in nombre_completo.split())

def generar_usuario(nombre, apellido):
    """ana.perez → para crear emails institucionales."""
    return f"{quitar_tildes(nombre).lower()}.{quitar_tildes(apellido).lower()}"

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for c in texto:
        if c.isalpha() and c.isascii():
            base = ord("A") if c.isupper() else ord("a")
            resultado += chr((ord(c) - base + desplazamiento) % 26 + base)
        else:
            resultado += c
    return resultado

def mascara_tarjeta(numero):
    return "*" * (len(numero) - 4) + numero[-4:]

print(es_palindromo("Anita lava la tina"), es_palindromo("Ecuador"))   # True False
print(contar_vocales("Murciélago"))                                    # 5
print(capitalizar_palabras("iNSTITUTO tecnológico ESPAÑA"))            # Instituto Tecnológico España
print(palabra_mas_larga("el desarrollo de software es genial"))        # desarrollo
print(iniciales("juan carlos pérez"))                                  # J.C.P.
print(generar_usuario("Andrés", "Núñez"))                              # andres.nunez
print(cifrado_cesar("Hola, Mundo", 3), cifrado_cesar(cifrado_cesar("Hola", 3), -3))  # Krod, Pxqgr Hola
print(mascara_tarjeta("4111111111111111"))                             # ************1111

# Formato de tablas en consola
datos = [("Ana", 9.2), ("Luis", 7.5), ("María Fernanda", 10)]
print(f"{'Nombre':<16}{'Nota':>6}")
print("-" * 22)
for n, nota in datos:
    print(f"{n:<16}{nota:>6.2f}")
