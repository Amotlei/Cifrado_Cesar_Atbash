import re
from collections import Counter

# ==========================================================
# ALFABETO
# ==========================================================
PATRON_PALABRAS = re.compile(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]+")

ALFABETO_DEFECTO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFABETO_ACTUAL = ALFABETO_DEFECTO

MAPA_IDX = {}
MAPA_REV = {}

def reconstruir_mapas():
    global MAPA_IDX, MAPA_REV
    MAPA_IDX = {c: i for i, c in enumerate(ALFABETO_ACTUAL)}
    MAPA_REV = {i: c for i, c in enumerate(ALFABETO_ACTUAL)}

reconstruir_mapas()


def es_letra(c):
    return c.isalpha()


def limpiar_texto(texto):
    return "".join(c for c in texto if es_letra(c) or c.isspace())


def normalizar_alfabeto(alfabeto):
    visto = set()
    resultado = []

    for c in alfabeto:
        if c not in visto:
            visto.add(c)
            resultado.append(c)

    return "".join(resultado)


def establecer_alfabeto(nuevo):
    global ALFABETO_ACTUAL

    if not nuevo:
        print("[!] Alfabeto vacío.")
        return

    nuevo = nuevo.upper()
    normalizado = normalizar_alfabeto(nuevo)

    if len(normalizado) < 2:
        print("[!] Alfabeto inválido.")
        return

    if len(normalizado) != len(nuevo):
        print("[!] Se eliminaron caracteres repetidos automáticamente.")

    ALFABETO_ACTUAL = normalizado
    reconstruir_mapas()

    print("[✓] Alfabeto activo:", ALFABETO_ACTUAL)


def restaurar_alfabeto():
    global ALFABETO_ACTUAL
    ALFABETO_ACTUAL = ALFABETO_DEFECTO
    reconstruir_mapas()
    print("[✓] Alfabeto restaurado.")


# ==========================================================
# CIFRADOS
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

def score_texto(texto):
    limpio = limpiar_texto(texto)

    tokens = PATRON_PALABRAS.findall(limpio.lower())
    total = len(tokens)

    # 1. Diccionario
    validas = sum(1 for t in tokens if t in DICT)
    ratio_diccionario = validas / total if total else 0

    # 2. Longitud promedio
    longitudes = [len(t) for t in tokens]
    if longitudes:
        promedio = sum(longitudes) / len(longitudes)
        score_longitud = 1 - abs(promedio - 5) / 5
    else:
        score_longitud = 0

    # 3. Proporción de letras
    letras = sum(1 for c in texto if c.isalpha())
    ratio_letras = letras / len(texto) if texto else 0

    # 4. Frecuencia de vocales
    vocales = "aeiou"
    total_letras = sum(1 for c in limpio.lower() if c.isalpha())
    if total_letras:
        freq_vocal = sum(1 for c in limpio.lower() if c in vocales) / total_letras
    else:
        freq_vocal = 0

    # 5. Penalización de ruido
    simbolos = sum(1 for c in texto if not c.isalnum() and not c.isspace())
    ratio_ruido = simbolos / len(texto) if texto else 0
    penalizacion_ruido = 1 - ratio_ruido

    score = (
        ratio_diccionario * 0.5 +
        score_longitud * 0.2 +
        ratio_letras * 0.1 +
        freq_vocal * 0.1 +
        penalizacion_ruido * 0.1
    )

    return score


# ==========================================================
# DETECCIÓN AVANZADA (TOP 3)
# ==========================================================

def detectar_cifrado(texto):
    resultados = []

    # Atbash
    intento = atbash(texto)
    resultados.append(("Atbash", intento, None, score_texto(intento)))

    # César
    for d in range(len(ALFABETO_ACTUAL)):
        dec = descifrar_cesar(texto, d)
        resultados.append(("Cesar", dec, d, score_texto(dec)))

    resultados.sort(key=lambda x: x[3], reverse=True)

    return resultados[:3]


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
            top = detectar_cifrado(txt)

            print("\n== MEJORES RESULTADOS ==")
            for tipo, res, d, sc in top:
                print("\nTipo:", tipo)
                if d is not None:
                    print("Desplazamiento:", d)
                print("Score:", round(sc, 3))

                if sc < 0.2:
                    print("[!] Baja confianza")

                print("Texto:", res)

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