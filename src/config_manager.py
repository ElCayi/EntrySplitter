#Contiene las funciones para cargar y guardar la configuración, así como la de configurar las entradas. 
# Se encarga de manejar el archivo JSON y validarlo.

# config_manager.py

import json
import os
from typing import Optional

CONFIG_FILE = "config_riesgo.json"

def cargar_configuracion() -> Optional[dict]:
    """
    Carga la configuración desde un archivo JSON y valida su estructura.
    Si está corrupta o no existe, retorna None.
    """
    if not os.path.exists(CONFIG_FILE):
        return None

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

        # Validar claves principales
        if "num_entradas" not in config or "entradas" not in config:
            raise ValueError("Faltan claves principales (num_entradas, entradas).")

        if not isinstance(config["num_entradas"], int) or config["num_entradas"] < 1:
            raise ValueError("num_entradas debe ser un entero positivo.")

        # Validar cada entrada
        for entrada in config["entradas"]:
            if (
                "peso" not in entrada or
                "stop_loss" not in entrada or
                not isinstance(entrada["peso"], (int, float)) or
                not isinstance(entrada["stop_loss"], (int, float)) or
                entrada["stop_loss"] <= 0
            ):
                raise ValueError(
                    "Cada entrada debe tener 'peso' numérico y 'stop_loss' (>0)."
                )
        return config

    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️ Configuración corrupta ({e}).")
        return None


def guardar_configuracion(config: dict) -> None:
    """Guarda la configuración en un archivo JSON con manejo de errores."""
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        print("✅ Configuración guardada correctamente.")
    except IOError:
        print("❌ Error: No se pudo guardar la configuración")


def configurar_entradas(obtener_entero, obtener_numero) -> dict:
    """
    Pide al usuario el número de entradas, luego las configura.
    (Si el usuario ingresa 'b' en medio, lanzará BackException automáticamente).
    """
    num_entradas = obtener_entero("🔢 Número de entradas (b=back): ", min_val=1)
    entradas = []
    
    for i in range(num_entradas):
        print(f"\n📊 Configuración Entrada {i+1}:")
        peso = obtener_numero("   Peso relativo (ej: 1, 2, 3, o 'b' para back): ")
        stop_loss = obtener_numero("   Stop loss (ej: 5 para 5%, o 'b' para back): ") / 100
        entradas.append({"peso": peso, "stop_loss": stop_loss})
    
    config = {"num_entradas": num_entradas, "entradas": entradas}
    guardar_configuracion(config)
    return config


def mostrar_configuracion(config: dict) -> None:
    """
    Muestra de forma sencilla la configuración actual.
    """
    print("\n🔥 Configuración actual:")
    print(f"  - Número de entradas: {config['num_entradas']}")
    for i, entrada in enumerate(config["entradas"], start=1):
        peso = entrada["peso"]
        stop_loss_pct = entrada["stop_loss"] * 100
        print(f"    {i}. Peso = {peso}, Stop loss = {stop_loss_pct:.2f}%")
