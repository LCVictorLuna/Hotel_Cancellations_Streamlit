import streamlit as st
import pandas as pd

from tabs import entender
from tabs import limpiar
from tabs import descriptiva
from tabs import predictiva
from tabs import prescriptiva
from tabs import decisiones


# Configuración de la página
st.set_page_config(
    page_title="Hotel Cancellation Analytics",
    page_icon="🏨",
    layout="wide"
)


# Carga de datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/reservas_hotel_sinteticas.csv")

df = cargar_datos()


# Encabezado
st.title("🏨 Hotel Cancellation Analytics")

st.write(
    """
    Esta aplicación analiza reservaciones hoteleras con el objetivo
    de identificar cuáles presentan mayor probabilidad de cancelación
    y apoyar la definición de acciones preventivas según su nivel
    de riesgo.
    """
)




# Crear las seis pestañas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Entender",
    "2. Limpiar",
    "3. Describir",
    "4. Predecir",
    "5. Prescribir",
    "6. Decidir"
])


# Pestaña 1
with tab1:
    entender.mostrar(df)


# Pestaña 2
with tab2:
    df_limpio = limpiar.mostrar(df)


# Pestaña 3
with tab3:
    descriptiva.mostrar(df_limpio)


# Pestaña 4
with tab4:
    modelo, variables_modelo = predictiva.mostrar(df_limpio)


# Pestaña 5
with tab5:
    resultados = prescriptiva.mostrar(
        df_limpio,
        modelo,
        variables_modelo
    )


# Pestaña 6
with tab6:
    decisiones.mostrar(resultados)