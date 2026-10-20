import streamlit as st
import pandas as pd


def mostrar(df):

    st.header("2. Limpiar los datos")

    st.subheader("¿Qué tan confiables son los datos?")

    st.write(
        """
        Antes de realizar el análisis es necesario revisar la calidad
        del dataset. En esta etapa se identifican valores nulos y
        registros duplicados, y se aplican decisiones de limpieza
        antes de continuar con el análisis.
        """
    )

    # Valores nulos
    st.subheader("Valores nulos")

    nulos = df.isnull().sum()

    tabla_nulos = pd.DataFrame({
        "Variable": nulos.index,
        "Valores nulos": nulos.values
    })

    st.dataframe(tabla_nulos)

    # Duplicados
    st.subheader("Registros duplicados")

    duplicados = df.duplicated().sum()

    st.metric(
        "Número de registros duplicados",
        duplicados
    )

    # Crear copia para limpieza
    df_limpio = df.copy()

    # Eliminar duplicados
    df_limpio = df_limpio.drop_duplicates()

    # Sustituir tarifa faltante por la mediana
    df_limpio["tarifa_diaria"] = (
        df_limpio["tarifa_diaria"]
        .fillna(df_limpio["tarifa_diaria"].median())
    )

    # Sustituir tipo de cliente faltante
    df_limpio["tipo_cliente"] = (
        df_limpio["tipo_cliente"]
        .fillna("No identificado")
    )

    # Resultado
    st.subheader("Resultado después de la limpieza")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Registros finales",
        len(df_limpio)
    )

    col2.metric(
        "Valores nulos",
        df_limpio.isnull().sum().sum()
    )

    col3.metric(
        "Duplicados",
        df_limpio.duplicated().sum()
    )

    return df_limpio