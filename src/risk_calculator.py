import pandas as pd
from tabulate import tabulate

def calculadora_riesgo(
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
    total_capital_en_riesgo = riesgo_max_porcentaje * total_capital

    # Verificar si las sumas son válidas y que todos los pesos son no negativos
    assert suma_pesos != 0, (
        "❌ Error: No se puede calcular el riesgo con sumas igual a 0."
    )
    assert all(peso >= 0 for peso in entradas["Peso"]), (
        "❌ Error: Todos los pesos deben ser no negativos."
    )

    entradas["Capital_En_Riesgo"] = total_capital_en_riesgo * (
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
