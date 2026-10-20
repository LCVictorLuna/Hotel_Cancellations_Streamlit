import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def mostrar(df):

    st.header("4. Estadística predictiva")

    st.subheader(
        "¿Podemos predecir qué reservaciones tienen mayor probabilidad de cancelarse?"
    )

    st.write(
        """
        En esta etapa se utiliza un modelo de regresión logística para
        estimar la probabilidad de cancelación de cada reservación.
        El modelo utiliza características disponibles antes de conocer
        el resultado de la reservación.
        """
    )

    # Variables predictoras
    variables_modelo = [
        "tipo_hotel",
        "dias_anticipacion",
        "noches_estancia",
        "numero_huespedes",
        "segmento_mercado",
        "tipo_cliente",
        "tipo_deposito",
        "tarifa_diaria",
        "solicitudes_especiales",
        "cancelaciones_previas"
    ]

    X = df[variables_modelo]
    y = df["cancelada"]

    # Variables numéricas

    variables_numericas = [
        "dias_anticipacion",
        "noches_estancia",
        "numero_huespedes",
        "tarifa_diaria",
        "solicitudes_especiales",
        "cancelaciones_previas"
    ]

    # Variables categóricas

    variables_categoricas = [
        "tipo_hotel",
        "segmento_mercado",
        "tipo_cliente",
        "tipo_deposito"
    ]

    # Preparación de variables

    preprocesador = ColumnTransformer([
        (
            "numericas",
            StandardScaler(),
            variables_numericas
        ),
        (
            "categoricas",
            OneHotEncoder(handle_unknown="ignore"),
            variables_categoricas
        )
    ])

    # Modelo predictivo con regresión logística

    modelo = Pipeline([
        ("preprocesamiento", preprocesador),
        ("modelo", LogisticRegression(max_iter=1000))
    ])

    # Separar datos de entrenamiento y prueba, se deciió el 20 % de prueba para tener un conjunto de datos suficiente para evaluar el modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Entrenar modelo
    modelo.fit(X_train, y_train)

    # Predicciones
    y_pred = modelo.predict(X_test)

    # Probabilidad de cancelación
    y_prob = modelo.predict_proba(X_test)[:, 1]

    # Métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    st.subheader("Resultados del modelo")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Accuracy",
        f"{accuracy:.1%}"
    )

    col2.metric(
        "Precision",
        f"{precision:.1%}"
    )

    col3.metric(
        "Recall",
        f"{recall:.1%}"
    )

    col4.metric(
        "F1-score",
        f"{f1:.1%}"
    )

    # Resultados de ejemplo
    st.subheader("Probabilidad estimada de cancelación")

    resultados = X_test.copy()

    resultados["Cancelación real"] = y_test.values
    resultados["Probabilidad de cancelación"] = y_prob

    resultados["Probabilidad de cancelación"] = (
        resultados["Probabilidad de cancelación"] * 100
    ).round(1)

    resultados = resultados.sort_values(
        "Probabilidad de cancelación",
        ascending=False
    )

    st.dataframe(
        resultados.head(20),
        use_container_width=True
    )



   
    # Encontrar Variables con mayor peso en la predicción
   

    st.subheader("Variables con mayor peso en la predicción")

    # Recuperar los nombres de las variables transformadas
    nombres_variables = modelo.named_steps[
        "preprocesamiento"
    ].get_feature_names_out()

    # Recuperar los coeficientes de la regresión logística
    coeficientes = modelo.named_steps[
        "modelo"
    ].coef_[0]

    # Crear una tabla con variables y coeficientes
    importancia = pd.DataFrame({
        "Variable": nombres_variables,
        "Coeficiente": coeficientes
    })

    # Calcular la magnitud del efecto
    importancia["Impacto absoluto"] = (
        importancia["Coeficiente"].abs()
    )

    # Ordenar de mayor a menor impacto
    importancia = importancia.sort_values(
        "Impacto absoluto",
        ascending=False
    )

    # Seleccionar las 10 variables con mayor peso
    top_variables = importancia.head(10).copy()

    # Ordenar para visualizar mejor el gráfico horizontal
    top_variables = top_variables.sort_values(
        "Coeficiente",
        ascending=True
    )

    # Gráfica de coeficientes
    st.bar_chart(
        top_variables,
        x="Variable",
        y="Coeficiente",
        horizontal=True
    )

    # Tabla de coeficientes
    st.dataframe(
        importancia.head(10),
        hide_index=True,
        use_container_width=True
    )

    # Devolver el modelo y las variables utilizadas
    return modelo, variables_modelo