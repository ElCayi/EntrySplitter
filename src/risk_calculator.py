import pandas as pd
import json
import os
import datetime
from tabulate import tabulate  # ✅ Ya instalado, no necesitamos verificarlo

CONFIG_FILE = "config_riesgo.json"

def obtener_numero(mensaje, min_val=1):
    """Solicita un número válido al usuario con reintentos."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < min_val:
                print(f"❌ Error: El valor debe ser mayor o igual a {min_val}")
                continue
            return valor
        except ValueError:
            print("❌ Error: Ingresa un número válido")


def obtener_entero(mensaje, min_val=1):
    """Solicita un número entero válido al usuario con reintentos."""
    while True:
        try:
            valor = int(obtener_numero(mensaje, min_val))
            return valor
        except ValueError:
            print("❌ Error: Ingresa un número entero")


def cargar_configuracion():
    """Carga la configuración guardada desde un archivo JSON, verificando su estructura y tipos de datos."""
    if not os.path.exists(CONFIG_FILE):
        return None

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

            # 🔍 Validar que las claves principales existan
            if "num_entradas" not in config or "entradas" not in config:
                raise ValueError("Formato inválido")

            # 🔍 Validar que num_entradas sea un entero positivo
            if not isinstance(config["num_entradas"], int) or config["num_entradas"] < 1:
                raise ValueError("El número de entradas debe ser un entero positivo.")

            # 🔍 Validar que cada entrada tenga valores numéricos
            for entrada in config["entradas"]:
                if (
                    "peso" not in entrada or "stop_loss" not in entrada or
                    not isinstance(entrada["peso"], (int, float)) or
                    not isinstance(entrada["stop_loss"], (int, float))
                ):
                    raise ValueError("Formato inválido en entradas: pesos y stop_loss deben ser numéricos.")

            return config

    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️ Configuración corrupta ({e}). Creando nueva...")
        return None


def guardar_configuracion(config):
    """Guarda la configuración en un archivo JSON con manejo de errores."""
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        print("✅ Configuración guardada correctamente.")
    except IOError:
        print("❌ Error: No se pudo guardar la configuración")


def configurar_entradas():
    """Permite configurar el número de entradas y sus valores."""
    num_entradas = obtener_entero("🔢 Número de entradas (debe ser un número entero): ", min_val=1)
    entradas = []
    
    for i in range(num_entradas):
        print(f"\n📊 Configuración Entrada {i+1}:")
        P = obtener_numero("   Peso relativo (ej: 1, 2, 3): ")
        S = obtener_numero("   Stop loss (ej: 5 para 5%): ") / 100
        entradas.append({"peso": P, "stop_loss": S})
    
    config = {"num_entradas": num_entradas, "entradas": entradas}
    guardar_configuracion(config)
    return config


def calcular_riesgo():
    print("\n" + "🌟"*30)
    print(" CALCULADOR DE RIESGO AVANZADO v3.1 ")
    print("🌟"*30 + "\n")

    C = obtener_numero("💰 Capital total (USD): ")
    R = obtener_numero("🎯 Riesgo máximo (ingrese 5 para 5%): ") / 100

    config = cargar_configuracion()
    if config:
        print("🔄 Configuración encontrada. Usando datos previos.")
        editar = input("⚙️ ¿Quieres modificar la configuración? (s/n): ").strip().lower()
        if editar in ['s', 'si', 'y', 'yes', 'ys']:
            config = configurar_entradas()
    else:
        print("⚠️ No hay configuración guardada. Creando nueva configuración...")
        config = configurar_entradas()

    num_entradas = config["num_entradas"]
    entradas = [(e["peso"], e["stop_loss"]) for e in config["entradas"]]

    sum_pesos = sum(p for p, s in entradas)
    sum_producto = sum(p * s for p, s in entradas)

    # 🔹 Preguntar solo una vez por el apalancamiento
    L = None
    modo_apalancamiento = input("\n⚖️ ¿Quieres calcular el apalancamiento automáticamente según un rango de precios? (s/n): ").strip().lower()

    if modo_apalancamiento in ['s', 'si', 'y', 'yes', 'ys']:
        min_precio = obtener_numero("📉 Precio mínimo esperado: ")
        max_precio = obtener_numero("📈 Precio máximo esperado: ")
    
        rango_precio = max_precio - min_precio
    
        if rango_precio == 0 or sum_producto == 0:
            print("\n❌ Error: El rango de precios o la suma de (peso * stop_loss) no pueden ser cero.")
            exit()

        L = (R * sum_pesos) / (sum_producto * rango_precio)
        print(f"\n✅ Apalancamiento óptimo calculado: {L:.2f}x")

    if L is None:
        L = obtener_numero("⚖️ Apalancamiento manual: ")

    if L > 50:  
        print("\n⚠️ Advertencia: El apalancamiento ingresado es muy alto (>50x).")
        ajustar = input("¿Quieres ajustar el apalancamiento? (s/n): ").strip().lower()
        if ajustar in ['s', 'si', 'y', 'yes']:
            L = obtener_numero("⚖️ Nuevo apalancamiento: ")

    k = (R * sum_pesos) / (L * sum_producto)

    resultados = []
    for i, (P, S) in enumerate(entradas, 1):
        C_entrada = k * (P / sum_pesos) * C
        riesgo = C_entrada * L * S
        resultados.append({
            "Entrada": i,
            "Capital": C_entrada,
            "Apalancado": C_entrada * L,
            "Riesgo USD": riesgo,
            "Riesgo %": (riesgo / C) * 100,
            "Stop %": S * 100
        })

    df = pd.DataFrame(resultados).set_index("Entrada")
    print("\n📊 Resultados detallados:")
    print(tabulate(df.round(2), headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    calcular_riesgo()
