import re

# ——————————————————————————————————————————
# Alfabeto (sin acentos)
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# ——————————————————————————————————————————
# Cifrado César
def cesar(texto, desplazamiento):
    texto_out = ""
    for c in texto:
        if c.upper() in ALFABETO:
            idx = ALFABETO.index(c.upper())
            idx2 = (idx + desplazamiento) % len(ALFABETO)
            letra = ALFABETO[idx2]
            texto_out += letra if c.isupper() else letra.lower()
        else:
            texto_out += c
    return texto_out

# Desencripta César
def descifrar_cesar(texto, desplazamiento):
    return cesar(texto, -desplazamiento % len(ALFABETO))


# ——————————————————————————————————————————
# Cifrado Atbash
def atbash(texto):
    texto_out = ""
    n = len(ALFABETO)
    for c in texto:
        if c.upper() in ALFABETO:
            idx = ALFABETO.index(c.upper())
            idx2 = n - 1 - idx
            letra = ALFABETO[idx2]
            texto_out += letra if c.isupper() else letra.lower()
        else:
            texto_out += c
    return texto_out


# ——————————————————————————————————————————
# Diccionario mínimo para validación
def cargar_diccionario():
    palabras = set()
    try:
        with open("diccionario.txt", "r", encoding="utf-8") as f:
            for linea in f:
                palabras.add(linea.strip().lower())
    except:
        print("[!] No se encontró diccionario.txt — se usará parcial.")
    return palabras

DICT = cargar_diccionario()


# ——————————————————————————————————————————
# Validación de palabras
def contar_palabras_validas(texto):
    tokens = re.findall(r"[A-Za-zÁÉÍÓÚÜáéíóúüñÑ]+", texto.lower())
    cnt = 0
    for t in tokens:
        if t in DICT:
            cnt += 1
    return cnt, len(tokens)


# ——————————————————————————————————————————
# Detección automática
def detectar_cifrado(texto):
    # Intentar Atbash
    intento_atbash = atbash(texto)
    ev_atbash = contar_palabras_validas(intento_atbash)

    # Intentar todos los desplazamientos César
    mejores = ("", "", 0, 0)  # (tipo, texto, cont_valido, desplazamiento)
    for d in range(len(ALFABETO)):
        dec = descifrar_cesar(texto, d)
        valido, total = contar_palabras_validas(dec)
        if valido > mejores[2]:
            mejores = ("Cesar", dec, valido, d)

    # Comparar con Atbash
    if ev_atbash[0] >= mejores[2]:
        return ("Atbash", intento_atbash, None)

    tipo, texto_desc, validas, despl = mejores
    return (tipo, texto_desc, despl)


# ——————————————————————————————————————————
# UI consola
def menu():
    print("=== CIFRADOR / DESCIFRADOR ===")
    print("1) Cifrar")
    print("2) Descifrar")
    print("3) Detectar & Descifrar")
    print("0) Salir")

def run():
    while True:
        menu()
        opc = input("> ")

        if opc == "1":
            txt = input("Texto a cifrar: ")
            d = int(input("Desplazamiento César (0–26): "))
            print("César ->", cesar(txt, d))
            print("Atbash ->", atbash(txt))
        elif opc == "2":
            txt = input("Texto a descifrar: ")
            m = input("Tipo (Cesar/Atbash): ").strip().lower()
            if m == "cesar":
                d = int(input("Desplazamiento usado: "))
                print(descifrar_cesar(txt, d))
            elif m == "atbash":
                print(atbash(txt))
            else:
                print("Tipo inválido.")
        elif opc == "3":
            txt = input("Texto cifrado: ")
            tipo, resultado, despl = detectar_cifrado(txt)
            print("== DETECTADO ==")
            print("Tipo:", tipo)
            if despl is not None:
                print("Desplazamiento:", despl)
            print("Descifrado:", resultado)
        elif opc == "0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    run()