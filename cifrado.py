import re
from collections import Counter

# ==========================================================
# ALFABETO
# ==========================================================

ALFABETO_DEFECTO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFABETO_ACTUAL = ALFABETO_DEFECTO

MAPA_IDX = {}
MAPA_REV = {}

def reconstruir_mapas():
    global MAPA_IDX, MAPA_REV
    MAPA_IDX = {c: i for i, c in enumerate(ALFABETO_ACTUAL)}
    MAPA_REV = {i: c for i, c in enumerate(ALFABETO_ACTUAL)}

reconstruir_mapas()


def establecer_alfabeto(nuevo):
    global ALFABETO_ACTUAL
    if not nuevo:
        print("[!] Alfabeto vacío.")
        return
    nuevo = nuevo.upper()
    if len(set(nuevo)) != len(nuevo):
        print("[!] Caracteres repetidos.")
        return
    ALFABETO_ACTUAL = nuevo
    reconstruir_mapas()
    print("[✓] Alfabeto personalizado activo.")


def restaurar_alfabeto():
    global ALFABETO_ACTUAL
    ALFABETO_ACTUAL = ALFABETO_DEFECTO
    reconstruir_mapas()
    print("[✓] Restaurado alfabeto por defecto.")


# ==========================================================
# CIFRADOS OPTIMIZADOS
# ==========================================================

def cesar(texto, d):
    n = len(ALFABETO_ACTUAL)
    res = []

    for c in texto:
        may = c.upper()
        if may in MAPA_IDX:
            idx = (MAPA_IDX[may] + d) % n
            letra = MAPA_REV[idx]
            res.append(letra if c.isupper() else letra.lower())
        else:
            res.append(c)

    return "".join(res)


def descifrar_cesar(texto, d):
    return cesar(texto, -d)


def atbash(texto):
    n = len(ALFABETO_ACTUAL)
    res = []

    for c in texto:
        may = c.upper()
        if may in MAPA_IDX:
            idx = n - 1 - MAPA_IDX[may]
            letra = MAPA_REV[idx]
            res.append(letra if c.isupper() else letra.lower())
        else:
            res.append(c)

    return "".join(res)


# ==========================================================
# DICCIONARIO
# ==========================================================

def cargar_diccionario():
    palabras = set()
    try:
        with open("diccionario.txt", "r", encoding="utf-8") as f:
            for linea in f:
                palabras.add(linea.strip().lower())
    except:
        print("[!] No se encontró diccionario.txt.")
    return palabras

DICT = cargar_diccionario()


# ==========================================================
# SCORING ROBUSTO
# ==========================================================

def generar_regex_dinamico():
    letras = "".join(
        c for c in ALFABETO_ACTUAL
        if c.isalpha()
    )
    if not letras:
        letras = "A-Za-z"
    return re.compile(f"[{re.escape(letras)}]+", re.IGNORECASE)


def score_texto(texto):
    patron = generar_regex_dinamico()
    tokens = patron.findall(texto)

    total = len(tokens)
    validas = sum(1 for t in tokens if t.lower() in DICT)

    ratio_diccionario = validas / total if total else 0

    letras = sum(1 for c in texto if c.upper() in ALFABETO_ACTUAL)
    ratio_letras = letras / len(texto) if texto else 0

    vocales = "AEIOU"
    freq = Counter(texto.upper())
    bonus_vocal = sum(freq[v] for v in vocales if v in freq) / len(texto) if texto else 0

    score = (
        ratio_diccionario * 0.6 +
        ratio_letras * 0.3 +
        bonus_vocal * 0.1
    )

    return score


# ==========================================================
# DETECTOR MEJORADO
# ==========================================================

def detectar_cifrado(texto):
    mejor_score = -1
    mejor = ("", texto, None)

    # Probar Atbash
    intento = atbash(texto)
    sc = score_texto(intento)
    if sc > mejor_score:
        mejor_score = sc
        mejor = ("Atbash", intento, None)

    # Probar César
    for d in range(len(ALFABETO_ACTUAL)):
        dec = descifrar_cesar(texto, d)
        sc = score_texto(dec)
        if sc > mejor_score:
            mejor_score = sc
            mejor = ("Cesar", dec, d)

    return mejor


# ==========================================================
# UI
# ==========================================================

def menu():
    print("\n=== CIFRADOR / DESCIFRADOR ===")
    print("Alfabeto actual:", ALFABETO_ACTUAL)
    print("1) Cifrar")
    print("2) Descifrar")
    print("3) Detectar & Descifrar")
    print("4) Establecer alfabeto personalizado")
    print("5) Restaurar alfabeto por defecto")
    print("0) Salir")


def run():
    while True:
        menu()
        opc = input("> ")

        if opc == "1":
            txt = input("Texto: ")
            d = int(input(f"Desplazamiento (0–{len(ALFABETO_ACTUAL)-1}): "))
            print("César ->", cesar(txt, d))
            print("Atbash ->", atbash(txt))

        elif opc == "2":
            txt = input("Texto: ")
            tipo = input("Tipo (Cesar/Atbash): ").lower()
            if tipo == "cesar":
                d = int(input("Desplazamiento: "))
                print(descifrar_cesar(txt, d))
            elif tipo == "atbash":
                print(atbash(txt))
            else:
                print("Tipo inválido.")

        elif opc == "3":
            txt = input("Texto cifrado: ")
            tipo, resultado, d = detectar_cifrado(txt)
            print("== DETECTADO ==")
            print("Tipo:", tipo)
            if d is not None:
                print("Desplazamiento:", d)
            print("Descifrado:", resultado)

        elif opc == "4":
            establecer_alfabeto(input("Nuevo alfabeto: "))

        elif opc == "5":
            restaurar_alfabeto()

        elif opc == "0":
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    run()