import streamlit as st
import pandas as pd


def mostrar(df, modelo, variables_modelo):

    st.header("5. Estadística prescriptiva")

    st.subheader(
        "¿Qué acción preventiva debería aplicarse a cada reservación?"
    )

    st.write(
        """
        En esta etapa, las probabilidades generadas por el modelo se
        convierten en niveles de riesgo. Cada nivel se relaciona con
        una acción preventiva para apoyar la gestión de las reservaciones
        y priorizar los recursos del hotel.
        """
    )

    
    # Calcular la probabilidad de cancelación para cada reservación
    

    resultados = df.copy()

    resultados["probabilidad_cancelacion"] = (
        modelo.predict_proba(
            resultados[variables_modelo]
        )[:, 1]
    )

    
    # Clasificar las reservaciones por nivel de riesgo
    

    resultados["nivel_riesgo"] = pd.cut(
        resultados["probabilidad_cancelacion"],
        bins=[0, 0.30, 0.60, 1.00],
        labels=[
            "Riesgo bajo",
            "Riesgo medio",
            "Riesgo alto"
        ],
        include_lowest=True
    )

    
    # Defiinir acciones recomendadas por nivel de riesgo
    

    acciones = {
        "Riesgo bajo":
            "Mantener la comunicación automática habitual.",

        "Riesgo medio":
            "Enviar recordatorio y ofrecer modificación de fechas.",

        "Riesgo alto":
            "Realizar contacto personalizado y solicitar confirmación."
    }

    resultados["accion_recomendada"] = (
        resultados["nivel_riesgo"]
        .astype(str)
        .map(acciones)
    )

    resultados["probabilidad_porcentaje"] = (
        resultados["probabilidad_cancelacion"] * 100
    ).round(1)

    
    # Resumen por nivel de riesgo
    

    st.subheader(
        "Distribución de reservaciones por nivel de riesgo"
    )

    total_bajo = (
        resultados["nivel_riesgo"] == "Riesgo bajo"
    ).sum()

    total_medio = (
        resultados["nivel_riesgo"] == "Riesgo medio"
    ).sum()

    total_alto = (
        resultados["nivel_riesgo"] == "Riesgo alto"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Riesgo bajo",
        f"{total_bajo:,}"
    )

    col2.metric(
        "Riesgo medio",
        f"{total_medio:,}"
    )

    col3.metric(
        "Riesgo alto",
        f"{total_alto:,}"
    )

    
    # Gráfico por niveles de riesgo
    

    distribucion_riesgo = (
        resultados["nivel_riesgo"]
        .value_counts()
        .reindex([
            "Riesgo bajo",
            "Riesgo medio",
            "Riesgo alto"
        ])
        .reset_index()
    )

    distribucion_riesgo.columns = [
        "Nivel de riesgo",
        "Número de reservaciones"
    ]

    st.bar_chart(
        distribucion_riesgo,
        x="Nivel de riesgo",
        y="Número de reservaciones"
    )

    
    # DEfinición de la acción recomendada
    

    st.subheader(
        "Acciones recomendadas por nivel de riesgo"
    )

    tabla_acciones = pd.DataFrame({
        "Nivel de riesgo": [
            "Riesgo bajo",
            "Riesgo medio",
            "Riesgo alto"
        ],

        "Probabilidad estimada": [
            "Menor o igual a 30 %",
            "Mayor a 30 % y hasta 60 %",
            "Mayor a 60 %"
        ],

        "Acción recomendada": [
            acciones["Riesgo bajo"],
            acciones["Riesgo medio"],
            acciones["Riesgo alto"]
        ]
    })

    st.dataframe(
        tabla_acciones,
        hide_index=True,
        use_container_width=True
    )

    
    # REcomendación por reservación
    

    st.subheader("Recomendación por reservación")

    filtro_riesgo = st.selectbox(
        "Selecciona el nivel de riesgo:",
        [
            "Todos",
            "Riesgo bajo",
            "Riesgo medio",
            "Riesgo alto"
        ],
        key="filtro_riesgo_prescriptiva"
    )

    # Crear copia para aplicar el filtro
    resultados_filtrados = resultados.copy()

    if filtro_riesgo != "Todos":
        resultados_filtrados = resultados_filtrados[
            resultados_filtrados["nivel_riesgo"] == filtro_riesgo
        ]

    # Columnas que se mostrarán
    columnas_resultado = [
        "id_reserva",
        "tipo_hotel",
        "segmento_mercado",
        "tipo_deposito",
        "probabilidad_porcentaje",
        "nivel_riesgo",
        "accion_recomendada"
    ]

    tabla_resultados = resultados_filtrados[
        columnas_resultado
    ].sort_values(
        "probabilidad_porcentaje",
        ascending=False
    )

    # Renombrar columnas para presentación
    tabla_resultados = tabla_resultados.rename(
        columns={
            "id_reserva":
                "ID de reservación",

            "tipo_hotel":
                "Tipo de hotel",

            "segmento_mercado":
                "Segmento de mercado",

            "tipo_deposito":
                "Tipo de depósito",

            "probabilidad_porcentaje":
                "Probabilidad de cancelación (%)",

            "nivel_riesgo":
                "Nivel de riesgo",

            "accion_recomendada":
                "Acción recomendada"
        }
    )

    st.dataframe(
        tabla_resultados,
        hide_index=True,
        use_container_width=True
    )

    
    # DEvolver resultados para la pestaña de decisiones
    

    return resultados