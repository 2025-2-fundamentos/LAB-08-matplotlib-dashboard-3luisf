

def pregunta_01():
    """Función principal que genera todas las visualizaciones."""
    # Crear directorio docs
    os.makedirs("docs", exist_ok=True)
    
    # Leer datos
    datos_df = pd.read_csv("files/input/shipping-data.csv")
    
    # Crear visualizaciones
    grafico_envios_por_bodega(datos_df)
    grafico_modo_envio(datos_df)
    grafico_promedio_calificacion_cliente(datos_df)
    grafico_distribucion_peso(datos_df)
    
    # Crear index.html
    generar_html_principal()

import os
import pandas as pd
import matplotlib.pyplot as plt


def grafico_envios_por_bodega(tabla):
    """Crea visualización de shipping por warehouse."""
    tabla = tabla.copy()
    plt.figure()
    conteos = tabla.Warehouse_block.value_counts()

    conteos.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record Count",
        color="tab:blue",
        fontsize=8,
    )

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.xticks(rotation=0)

    plt.savefig("docs/shipping_per_warehouse.png")
    plt.close()


def grafico_modo_envio(tabla):
    """Crea visualización de modo de envío."""
    tabla = tabla.copy()
    plt.figure()
    conteos = tabla.Mode_of_Shipment.value_counts()
    
    conteos.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"]
    )

    plt.savefig("docs/mode_of_shipment.png")
    plt.close()


def grafico_promedio_calificacion_cliente(tabla):
    """Crea visualización de rating promedio de clientes."""
    tabla = tabla.copy()
    plt.figure()

    agrupado = (
        tabla[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )

    agrupado.columns = agrupado.columns.droplevel()
    agrupado = agrupado[["mean", "min", "max"]]

    plt.barh(
        y=agrupado.index.values,
        width=agrupado["max"].values - 1,
        left=agrupado["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8
    )

    colores = [
        "tab:green" if valor >= 3.0 else "tab:orange" 
        for valor in agrupado["mean"].values
    ]

    plt.barh(
        y=agrupado.index.values,
        width=agrupado["mean"].values - 1,
        left=agrupado["min"].values,
        color=colores,
        height=0.5,
        alpha=1.0
    )

    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig("docs/average_customer_rating.png")
    plt.close()


def grafico_distribucion_peso(tabla):
    """Crea visualización de distribución de peso."""
    tabla = tabla.copy()
    plt.figure()

    tabla.Weight_in_gms.plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white"
    )

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig("docs/weight_distribution.png")
    plt.close()


def generar_html_principal():
    """Crea el archivo index.html con las visualizaciones."""
    contenido_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shipping Data Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; }
        .chart { margin: 20px; text-align: center; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Shipping Data Dashboard</h1>
    <div class="container">
        <div class="chart">
            <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">
        </div>
        <div class="chart">
            <img src="mode_of_shipment.png" alt="Mode of Shipment">
        </div>
        <div class="chart">
            <img src="average_customer_rating.png" alt="Average Customer Rating">
        </div>
        <div class="chart">
            <img src="weight_distribution.png" alt="Weight Distribution">
        </div>
    </div>
</body>
</html>"""
    
    with open("docs/index.html", "w", encoding="utf-8") as archivo:
        archivo.write(contenido_html)

pregunta_01()
