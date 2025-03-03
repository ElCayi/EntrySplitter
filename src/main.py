import sys
import logging

from io_utils import obtener_numero, obtener_entero, BackException
from config_manager import (
    cargar_configuracion,
    configurar_entradas,
    mostrar_configuracion
)
from risk_calculator import calculadora_riesgo

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("""
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
   CALCULADORA DE RIESGO v5.0
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
""")

    while True:
        try:
            config = cargar_configuracion()
            if config:
                mostrar_configuracion(config)
            else:
                print("⚠️ No hay configuración previa o está corrupta.")
                config = configurar_entradas(obtener_entero, obtener_numero)

            print("\n🦑 ¿Qué deseas hacer?")
            print("1. Usar esta configuración")
            print("2. Modificar")
            print("b. Volver a inicio (reiniciar el ciclo)")
            
            accion = input("> ").strip().lower()

            if accion == 'b':
                print("Volviendo al inicio...\n")
                continue

            if accion == "2":
                config = configurar_entradas(obtener_entero, obtener_numero)
                mostrar_configuracion(config)

            total_capital = obtener_numero("💰 Capital total (USD) (o 'b' para atrás): ", min_val=0.01)
            logging.debug(f"Capital total ingresado: {total_capital}")

            riesgo_input = obtener_numero("🎯 Riesgo máximo (ej: 5 para 5%) (b=back): ", min_val=0.01)
            riesgo_max_porcentaje = riesgo_input / 100
            logging.debug(f"Riesgo máximo ingresado: {riesgo_input}% -> {riesgo_max_porcentaje} en decimal")

            calculadora_riesgo(config, total_capital, riesgo_max_porcentaje)

            repetir = input("¿Quieres hacer otro cálculo? (s/n): ").strip().lower()
            if repetir not in ['s', 'si', 'y', 'yes']:
                print("Saliendo del programa...")
                sys.exit(0)

        except BackException:
            print("🔙 Regresando al inicio del programa...\n")
            continue

if __name__ == "__main__":
    main()
