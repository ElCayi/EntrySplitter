# Contiene la lógica pura para el cálculo de riesgo. Observa que hemos separado
# la lógica de la interacción con el usuario.

# risk_calculator.py
import pandas as pd
from tabulate import tabulate


def calculadora_riesgo_v4(
    config: dict, total_capital: float, riesgo_max_porcentaje: float, leverage: int
) -> None:
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
        resultados.append(
            {
                "Entrada": i,
                "Capital": capital_entrada,
                "Apalancado": capital_entrada * leverage,
                "Leverage": leverage,
                "Riesgo USD": riesgo_usd,
                "Riesgo %": (riesgo_usd / total_capital) * 100,
                "Stop %": stop_loss * 100,
            }
        )

    df = pd.DataFrame(resultados).set_index("Entrada")
    df_print = df.copy()
    for col in df_print.columns:
        if col != "Leverage":
            df_print[col] = df_print[col].round(2)
    df_print["Leverage"] = df_print["Leverage"].astype(int)

    print("\n📊 Resultados detallados:")
    print(tabulate(df_print, headers="keys", tablefmt="grid"))
    print()


def calculadora_riesgo_v5(
    config: dict, total_capital: float, riesgo_max_porcentaje: float
) -> None:
    """
    CALCULADORA DE RIESGO v5.0
    Calcula y muestra la distribución de capital y el riesgo resultante.
    """
    # Crear un DataFrame con las entradas
    entradas = pd.DataFrame(
        [(e["peso"], e["stop_loss"]) for e in config["entradas"]],
        columns=["Peso", "Stop_Loss"],
    )

    # Calcular el capital en riesgo y el capital apalancado idóneo
    suma_pesos = sum(peso for peso in entradas["Peso"])
    total_capital_en_riego = riesgo_max_porcentaje * total_capital

    # Verificar si las sumas son válidas y que todos los pesos son no negativos
    assert suma_pesos != 0, (
        "❌ Error: No se puede calcular el riesgo con sumas igual a 0."
    )
    assert all(peso >= 0 for peso in entradas["Peso"]), (
        "❌ Error: Todos los pesos deben ser no negativos."
    )

    entradas["Capital_En_Riesgo"] = total_capital_en_riego * (
        entradas["Peso"] / suma_pesos
    )
    entradas["Capital_Entrada_Apalancado_Idoneo"] = (
        entradas["Capital_En_Riesgo"] / entradas["Stop_Loss"]
    )
    entradas["Capital_Disponible"] = total_capital * (entradas["Peso"] / suma_pesos)
    entradas["Leverage"] = 0

    capital_entrada_sin_asignar = total_capital
    capital_entrada_sin_asignar_fue_modificado = True

    # Asignar el leverage inicial
    while (
        capital_entrada_sin_asignar > 0 and capital_entrada_sin_asignar_fue_modificado
    ):
        capital_entrada_sin_asignar_fue_modificado = False
        suma_pesos_sin_asignar = 0

        # Iterar sobre las entradas sin leverage asignado
        for i, row in entradas[entradas["Leverage"] == 0].iterrows():
            if row["Capital_Entrada_Apalancado_Idoneo"] <= row["Capital_Disponible"]:
                capital_entrada_sin_asignar -= row["Capital_Entrada_Apalancado_Idoneo"]
                entradas.at[i, "Leverage"] = 1
                capital_entrada_sin_asignar_fue_modificado = True
            else:
                suma_pesos_sin_asignar += row["Peso"]

        # Recalcular el capital disponible para las entradas sin leverage asignado
        if suma_pesos_sin_asignar > 0:
            entradas.loc[entradas["Leverage"] == 0, "Capital_Disponible"] = (
                capital_entrada_sin_asignar
                * (entradas["Peso"] / suma_pesos_sin_asignar)
            )

    MAX_LEVERAGE = 100
    # Asignar el leverage final
    for i, row in entradas.iterrows():
        if row["Leverage"] == 0:
            entradas.at[i, "Leverage"] = min(
                row["Capital_Entrada_Apalancado_Idoneo"] // row["Capital_Disponible"],
                MAX_LEVERAGE,
            )

    # Crear la tabla de resultados
    resultados = pd.DataFrame()
    resultados["Entrada"] = entradas.index + 1
    resultados["Capital"] = (
        entradas["Capital_Entrada_Apalancado_Idoneo"] / entradas["Leverage"]
    )
    resultados["Apalancado"] = resultados["Capital"] * entradas["Leverage"]
    resultados["Leverage"] = entradas["Leverage"]
    resultados["Riesgo USD"] = resultados["Apalancado"] * entradas["Stop_Loss"]
    resultados["Riesgo %"] = (resultados["Riesgo USD"] / total_capital) * 100
    resultados["Stop %"] = entradas["Stop_Loss"] * 100

    # Reorganizar las columnas
    resultados = resultados[
        [
            "Entrada",
            "Capital",
            "Apalancado",
            "Leverage",
            "Riesgo USD",
            "Riesgo %",
            "Stop %",
        ]
    ].set_index("Entrada")

    # Redondear los valores y ajustar el tipo de dato de la columna "Leverage"
    for col in resultados.columns:
        if col != "Leverage":
            resultados[col] = resultados[col].round(2)
    resultados["Leverage"] = resultados["Leverage"].astype(int)

    print("\n📊 Resultados detallados:")
    print(tabulate(resultados, headers="keys", tablefmt="grid"))
    print()