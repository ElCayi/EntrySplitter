import sys
import logging

from io_utils import obtener_numero, obtener_entero, BackException
from config_manager import (
    cargar_configuracion,
    configurar_entradas,
    mostrar_configuracion
)
from risk_calculator import calculadora_riesgo_v4

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("""
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
   CALCULADORA DE RIESGO v4.0
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

            modo_apalancamiento = input("\n⚖️ ¿Calcular apalancamiento automáticamente? (s/n/b=back): ").strip().lower()
            if modo_apalancamiento == 'b':
                print("Volviendo al menú...\n")
                continue

            if modo_apalancamiento in ['s', 'si', 'y', 'yes']:
                while True:
                    precio_minimo = obtener_numero("📉 Precio mínimo esperado (b=back): ", min_val=0.0)
                    precio_maximo = obtener_numero("📈 Precio máximo esperado (b=back): ", min_val=0.0)
                    rango_precio = precio_maximo - precio_minimo
                    logging.debug(f"Precio mínimo: {precio_minimo}, Precio máximo: {precio_maximo}, Rango: {rango_precio}")

                    if rango_precio <= 0:
                        print("❌ Error: El precio máximo debe ser mayor que el mínimo.")
                        continue

                    entradas = config["entradas"]
                    suma_pesos = sum(e["peso"] for e in entradas)
                    suma_producto = sum(e["peso"] * e["stop_loss"] for e in entradas)

                    logging.debug(f"Suma de pesos: {suma_pesos}")
                    logging.debug(f"Suma de productos (peso * stop_loss): {suma_producto}")

                    if suma_producto == 0:
                        print("❌ Error: La suma de (peso * stop_loss) es cero. Verifica la configuración.")
                        break

                    leverage_float = (riesgo_max_porcentaje * suma_pesos) / (suma_producto * rango_precio)
                    leverage = max(1, int(round(leverage_float)))
                    logging.debug(f"Apalancamiento calculado: {leverage_float} -> {leverage}x")

                    print(f"✅ Apalancamiento calculado (aprox.): {leverage}x")
                    break
            else:
                leverage_ingresado = obtener_numero("⚖️ Apalancamiento manual (b=back): ", min_val=0.01)
                leverage = max(1, int(round(leverage_ingresado)))
                logging.debug(f"Apalancamiento ingresado manualmente: {leverage_ingresado} -> {leverage}x")

            if leverage > 50:
                print("\n⚠️ Advertencia: El apalancamiento ingresado es muy alto (>50x).")
                ajustar = input("¿Quieres ajustar el apalancamiento? (s/n/b=back): ").strip().lower()
                if ajustar == 'b':
                    print("Volviendo al menú...\n")
                    continue
                if ajustar in ['s', 'si', 'y', 'yes']:
                    leverage_ingresado = obtener_numero("⚖️ Nuevo apalancamiento (b=back): ", min_val=0.01)
                    leverage = max(1, int(round(leverage_ingresado)))
                    logging.debug(f"Nuevo apalancamiento ajustado: {leverage_ingresado} -> {leverage}x")

            calculadora_riesgo_v4(config, total_capital, riesgo_max_porcentaje, leverage)

            repetir = input("¿Quieres hacer otro cálculo? (s/n): ").strip().lower()
            if repetir not in ['s', 'si', 'y', 'yes']:
                print("Saliendo del programa...")
                sys.exit(0)

        except BackException:
            print("🔙 Regresando al inicio del programa...\n")
            continue

if __name__ == "__main__":
    main()
