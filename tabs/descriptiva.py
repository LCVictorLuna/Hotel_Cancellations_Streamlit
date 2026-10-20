import streamlit as st
import pandas as pd


def mostrar(df):

    st.header("3. Estadística descriptiva")

    st.subheader(
        "¿Cómo se comportan las reservaciones y qué segmentos "
        "presentan mayor cancelación?"
    )

    st.write(
        """
        En esta etapa se analizan los principales indicadores del
        dataset limpio y se comparan las tasas de cancelación entre
        diferentes segmentos. El objetivo es identificar patrones
        relevantes antes de construir el modelo predictivo.
        """
    )

    
    # KPIs 
    

    st.subheader("Indicadores principales")

    total_reservaciones = len(df)

    tasa_cancelacion = (
        df["cancelada"].mean() * 100
    )

    anticipacion_promedio = (
        df["dias_anticipacion"].mean()
    )

    tarifa_promedio = (
        df["tarifa_diaria"].mean()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Reservaciones analizadas",
        f"{total_reservaciones:,}"
    )

    col2.metric(
        "Tasa de cancelación",
        f"{tasa_cancelacion:.1f}%"
    )

    col3.metric(
        "Anticipación promedio",
        f"{anticipacion_promedio:.0f} días"
    )

    col4.metric(
        "Tarifa diaria promedio",
        f"${tarifa_promedio:,.2f}"
    )

    
    # Cancelación por segmento de mercado
    

    st.subheader(
        "Tasa de cancelación por segmento de mercado"
    )

    cancelacion_segmento = (
        df.groupby("segmento_mercado")["cancelada"]
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=False)
        .reset_index()
    )

    cancelacion_segmento.columns = [
        "Segmento de mercado",
        "Tasa de cancelación"
    ]

    st.bar_chart(
        cancelacion_segmento,
        x="Segmento de mercado",
        y="Tasa de cancelación"
    )

    st.dataframe(
        cancelacion_segmento,
        hide_index=True,
        use_container_width=True
    )

    
    # Cancelación por tipo de depósito
    

    st.subheader(
        "Tasa de cancelación por tipo de depósito"
    )

    cancelacion_deposito = (
        df.groupby("tipo_deposito")["cancelada"]
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=False)
        .reset_index()
    )

    cancelacion_deposito.columns = [
        "Tipo de depósito",
        "Tasa de cancelación"
    ]

    st.bar_chart(
        cancelacion_deposito,
        x="Tipo de depósito",
        y="Tasa de cancelación"
    )

    st.dataframe(
        cancelacion_deposito,
        hide_index=True,
        use_container_width=True
    )

    
    # Cancelación por tipo de hotel
    

    st.subheader(
        "Tasa de cancelación por tipo de hotel"
    )

    cancelacion_hotel = (
        df.groupby("tipo_hotel")["cancelada"]
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=False)
        .reset_index()
    )

    cancelacion_hotel.columns = [
        "Tipo de hotel",
        "Tasa de cancelación"
    ]

    st.bar_chart(
        cancelacion_hotel,
        x="Tipo de hotel",
        y="Tasa de cancelación"
    )

    st.dataframe(
        cancelacion_hotel,
        hide_index=True,
        use_container_width=True
    )