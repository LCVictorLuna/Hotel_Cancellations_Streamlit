Hotel Cancellation Analytics
Proyecto académico de Ciencia de Datos desarrollado en Python y Streamlit para analizar el riesgo de cancelación de reservaciones hoteleras y apoyar la toma de decisiones.

Pregunta de negocio
¿Qué reservaciones tienen mayor probabilidad de ser canceladas y qué acción preventiva debería aplicar el hotel en cada nivel de riesgo?

Metodología
La aplicación sigue seis etapas:

Entender los datos
Limpiar los datos
Estadística descriptiva
Estadística predictiva
Estadística prescriptiva
Toma de decisiones
Dataset
La aplicación utiliza un dataset sintético de reservaciones hoteleras construido con fines académicos.

La estructura y las distribuciones fueron desarrolladas tomando como referencia el dataset público Hotel Booking Demand disponible en Kaggle.

Los datos sintéticos no representan huéspedes reales ni contienen información personal.

Modelo predictivo
Se utiliza un modelo de regresión logística para estimar la probabilidad de cancelación de cada reservación.

Posteriormente, las probabilidades se clasifican en tres niveles de riesgo:

Riesgo bajo
Riesgo medio
Riesgo alto
Cada nivel tiene asociada una acción preventiva para apoyar la toma de decisiones.

Tecnologías
Python 3.12.10
Streamlit
pandas
NumPy
scikit-learn
Ejecución
Instalar las dependencias:

pip install -r requirements.txt

Ejecutar la aplicación:

streamlit run app.py