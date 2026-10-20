import streamlit as st
import pandas as pd


def mostrar(df):

    st.header("1. Entender los datos")

    st.subheader(
        "¿Quiénes son nuestros casos y qué información tenemos?"
    )

    st.write(
        """
        Cada registro representa una reservación hotelera anonimizada.
        En esta primera etapa se revisa el tamaño del dataset, las
        variables disponibles y los tipos de datos antes de realizar
        cualquier transformación.
        """
    )

    # Métricas principales
    st.subheader("Resumen del dataset")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Número de registros",
        len(df)
    )

    col2.metric(
        "Número de variables",
        len(df.columns)
    )

    col3.metric(
        "Tasa de cancelación",
        f"{df['cancelada'].mean() * 100:.1f}%"
    )

    # Vista previa
    st.subheader("Vista previa del dataset")

    st.dataframe(df.head())

    # Variables disponibles
    st.subheader("Variables disponibles")
    
    # Linea cambiada MC - 4

    #st.write(df.columns.tolist())

    variables = pd.DataFrame({
    "Variable": df.columns
    })

    st.dataframe(
    variables,
    hide_index=True,
    use_container_width=True
    )

    # Tipos de datos
    st.subheader("Tipos de datos")

    tipos_datos = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": df.dtypes.astype(str).values
    })

    st.dataframe(
        tipos_datos,
        hide_index=True,
        use_container_width=True
    )

    