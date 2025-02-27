#Contiene la lógica pura para el cálculo de riesgo. Observa que hemos separado 
# la lógica de la interacción con el usuario.

# risk_calculator.py
import pandas as pd
from tabulate import tabulate

def calculadora_riesgo_v4(config: dict, total_capital: float, riesgo_max_porcentaje: float, leverage: int) -> None:
    """
    CALCULADORA DE RIESGO v4.0
    Calcula y muestra la distribución de capital y el riesgo resultante.
    """
    entradas = [(e["peso"], e["stop_loss"]) for e in config["entradas"]]
    suma_pesos = sum(peso for peso, _ in entradas)
    suma_producto = sum(peso * stop_loss for peso, stop_loss in entradas)

    if suma_pesos == 0 or suma_producto == 0:
        print("\n❌ Error: No se puede calcular el riesgo con sumas igual a 0.")
        return

    factor_base = (riesgo_max_porcentaje * suma_pesos) / (leverage * suma_producto)

    resultados = []
    for i, (peso, stop_loss) in enumerate(entradas, start=1):
        capital_entrada = factor_base * (peso / suma_pesos) * total_capital
        riesgo_usd = capital_entrada * leverage * stop_loss
        resultados.append({
            "Entrada": i,
            "Capital": capital_entrada,
            "Apalancado": capital_entrada * leverage,
            "Leverage": leverage,
            "Riesgo USD": riesgo_usd,
            "Riesgo %": (riesgo_usd / total_capital) * 100,
            "Stop %": stop_loss * 100
        })

    df = pd.DataFrame(resultados).set_index("Entrada")
    df_print = df.copy()
    for col in df_print.columns:
        if col != "Leverage":
            df_print[col] = df_print[col].round(2)
    df_print["Leverage"] = df_print["Leverage"].astype(int)

    print("\n📊 Resultados detallados:")
    print(tabulate(df_print, headers="keys", tablefmt="grid"))
    print()
