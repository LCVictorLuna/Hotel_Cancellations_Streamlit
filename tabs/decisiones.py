import streamlit as st


def mostrar(resultados):

    st.header("6. Toma de decisiones")

    st.subheader(
        "¿Qué decisión y mensaje deberíamos aplicar a cada nivel de riesgo?"
    )

    st.write(
        """
        En esta etapa se transforman los resultados del análisis en una
        decisión de negocio. El usuario puede seleccionar un nivel de
        riesgo y consultar la acción recomendada, un mensaje sugerido
        para el huésped y la justificación de la decisión.
        """
    )

    
    # Selección de nivel de riesgo
    

    nivel = st.selectbox(
        "Selecciona un nivel de riesgo:",
        [
            "Riesgo bajo",
            "Riesgo medio",
            "Riesgo alto"
        ],
        key="nivel_riesgo_decisiones"
    )

    
    # Filtrar los resultados 
    

    segmento = resultados[
        resultados["nivel_riesgo"] == nivel
    ]

    total_reservaciones = len(segmento)

    probabilidad_promedio = (
        segmento["probabilidad_cancelacion"].mean() * 100
    )

    
    # Información segú nivel de riesgo
    

    if nivel == "Riesgo bajo":

        accion = (
            "Mantener la comunicación automática habitual."
        )

        mensaje = (
            "Su reservación está confirmada. "
            "Esperamos recibirle próximamente y continuaremos "
            "compartiendo la información necesaria para su estancia."
        )

        justificacion = (
            "La probabilidad estimada de cancelación es baja, "
            "por lo que no se considera necesario realizar un "
            "seguimiento adicional. La recomendación es mantener "
            "la comunicación habitual y evitar utilizar recursos "
            "adicionales en este grupo."
        )

    elif nivel == "Riesgo medio":

        accion = (
            "Enviar un recordatorio y ofrecer la posibilidad "
            "de modificar las fechas."
        )

        mensaje = (
            "Su próxima estancia se acerca. Si necesita realizar "
            "algún cambio en las fechas de su reservación, puede "
            "contactarnos para revisar las alternativas disponibles."
        )

        justificacion = (
            "La reservación presenta un nivel intermedio de riesgo. "
            "Una comunicación preventiva puede ayudar a identificar "
            "posibles cambios con anticipación antes de que se "
            "produzca una cancelación."
        )

    else:

        accion = (
            "Realizar contacto personalizado y solicitar "
            "confirmación de la reservación."
        )

        mensaje = (
            "Queremos confirmar los detalles de su próxima estancia. "
            "Si sus planes han cambiado o requiere realizar algún "
            "ajuste, podemos apoyarle con las alternativas disponibles."
        )

        justificacion = (
            "La reservación presenta una probabilidad estimada de "
            "cancelación superior al umbral definido para riesgo alto. "
            "Por ello se recomienda priorizar el contacto y confirmar "
            "la intención de mantener la reservación."
        )

    
    # Resumen del Segmento 
    

    st.subheader("Resumen del nivel seleccionado")

    col1, col2 = st.columns(2)

    col1.metric(
        "Reservaciones en este nivel",
        f"{total_reservaciones:,}"
    )

    col2.metric(
        "Probabilidad promedio de cancelación",
        f"{probabilidad_promedio:.1f}%"
    )

    
    # DEcisión REcomendada 
    

    st.subheader("Acción recomendada")

    st.success(accion)

    
    # sugerencia de mendaje para el huesped que reservó
    

    st.subheader("Mensaje sugerido")

    st.info(mensaje)

    
    # Justificación de la decisión
    

    st.subheader("Justificación de la decisión")

    st.write(justificacion)

    
    # Ejemplos de reservaiones del segmento 
    

    st.subheader("Ejemplos de reservaciones")

    ejemplos = segmento[
        [
            "id_reserva",
            "tipo_hotel",
            "segmento_mercado",
            "tipo_deposito",
            "probabilidad_porcentaje"
        ]
    ].copy()

    ejemplos = ejemplos.rename(
        columns={
            "id_reserva": "ID de reservación",
            "tipo_hotel": "Tipo de hotel",
            "segmento_mercado": "Segmento de mercado",
            "tipo_deposito": "Tipo de depósito",
            "probabilidad_porcentaje":
                "Probabilidad de cancelación (%)"
        }
    )

    ejemplos = ejemplos.sort_values(
        "Probabilidad de cancelación (%)",
        ascending=False
    )

    st.dataframe(
        ejemplos.head(10),
        hide_index=True,
        use_container_width=True
    )

    