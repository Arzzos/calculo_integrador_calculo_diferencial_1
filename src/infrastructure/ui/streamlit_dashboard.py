# Contiene la interfaz de usuario construida con Streamlit. Es la capa de presentación.
# Se encarga de recibir la entrada del usuario, llamar a los casos de uso y mostrar los resultados.

import streamlit as st               # st es el módulo principal de Streamlit para construir la UI.
import plotly.graph_objects as go    # go es el módulo de Plotly para crear gráficos.
import numpy as np                   # Librería para operaciones numéricas (arreglos, funciones matemáticas).
from src.application.dtos import FunctionInputDTO   # DTO de entrada para el caso de uso.
from src.application.use_cases import EvaluateFunctionUseCase, GeneratePlotDataUseCase
from src.infrastructure.math_engine import SympyEvaluatorAdapter
from src.domain.exceptions import InvalidExpressionError

def main():
    """
    Función principal que construye la interfaz de usuario.
    Esta función es llamada desde app.py.
    """

    # Configuración de la página: título, icono (sin emoji) y layout ancho.
    st.set_page_config(
        page_title="Motor Interactivo de Análisis de Funciones",  # Título en la pestaña del navegador.
        page_icon="⌠",           # Icono que aparece en la pestaña (símbolo de integral, sin emoji).
        layout="wide"            # Layout de ancho completo para aprovechar el espacio.
    )

    # Títulos mostrados en la página.
    st.title("Analisis y Graficacion de Funciones")          # Encabezado principal.
    st.markdown("### Proyecto Integrador - Calculo Diferencial")  # Subtítulo con markdown.

    # Se instancian los objetos necesarios para la lógica de negocio.
    evaluator = SympyEvaluatorAdapter()   # Adaptador concreto para evaluar expresiones con SymPy.
    evaluate_use_case = EvaluateFunctionUseCase(evaluator)   # Caso de uso para evaluar la función.
    generate_plot_use_case = GeneratePlotDataUseCase()       # Caso de uso para preparar datos para el gráfico.

    # --- Barra lateral (Sidebar) donde el usuario ingresa los datos ---
    with st.sidebar:
        st.header("Configuracion de la Funcion")  # Encabezado de la sección.

        # Campo de texto para ingresar la expresión matemática.
        expression = st.text_input(
            "Expresion f(x)",                           # Etiqueta del campo.
            value="x**3 - 3*x + 2",                     # Valor por defecto.
            help="Ingresa una funcion en terminos de 'x'. Ejemplo: sin(x), exp(x), log(x), etc."  # Ayuda emergente.
        )

        st.subheader("Dominio de evaluacion")          # Subtítulo para los controles del dominio.

        # Dos columnas para ingresar x_min y x_max.
        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input(
                "x_min",           # Etiqueta.
                value=-5.0,        # Valor inicial.
                step=0.5,          # Incremento/decremento al hacer clic en las flechas.
                format="%.2f"      # Formato con dos decimales.
            )
        with col2:
            x_max = st.number_input(
                "x_max",
                value=5.0,
                step=0.5,
                format="%.2f"
            )

        # Control deslizante para seleccionar el número de puntos a evaluar.
        num_points = st.slider(
            "Numero de puntos",
            min_value=10,
            max_value=1000,
            value=200,
            step=10,
            help="Resolucion de la curva. Mas puntos dan una grafica mas suave."
        )

    # Validación básica: el mínimo debe ser menor que el máximo.
    if x_min >= x_max:
        st.error("El valor de x_min debe ser menor que x_max.")  # Mensaje de error en rojo.
        st.stop()   # Detiene la ejecución del script para no continuar con valores inválidos.

    # --- Ejecutar el caso de uso de evaluación ---
    try:
        # Se construye el DTO de entrada con los datos del usuario.
        input_dto = FunctionInputDTO(
            expression=expression,
            x_min=x_min,
            x_max=x_max,
            num_points=num_points
        )
        # Se ejecuta el caso de uso que evalúa la función y devuelve un DTO con resultados.
        result = evaluate_use_case.execute(input_dto)
        # Se preparan los datos para el gráfico (prácticamente pasa los mismos datos).
        plot_data = generate_plot_use_case.execute(result)

        # --- Mostrar la función en formato LaTeX ---
        st.subheader("Funcion ingresada")
        st.latex(f"f(x) = {result.latex}")  # st.latex renderiza la expresión matemática con LaTeX.

        # --- Pestañas para organizar el contenido (futuras fases) ---
        tab1, tab2, tab3, tab4 = st.tabs([
            "Explorador de Funciones",
            "Limites (Proximamente)",
            "Derivadas (Proximamente)",
            "Optimizacion (Proximamente)"
        ])

        with tab1:
            # Crear la figura de Plotly.
            fig = go.Figure()
            # Añadir una traza: puntos y línea.
            fig.add_trace(go.Scatter(
                x=result.x_values,          # Lista de valores de x.
                y=result.y_values,          # Lista de valores de f(x).
                mode='lines+markers',       # Dibuja línea y marcadores.
                name=f'f(x) = {expression}', # Nombre de la serie.
                marker=dict(size=3),        # Tamaño de los marcadores.
                line=dict(width=2)          # Ancho de la línea.
            ))

            # Configurar el diseño del gráfico.
            fig.update_layout(
                title=f"Grafica de {expression}",
                xaxis_title="x",
                yaxis_title="f(x)",
                hovermode="x unified",      # Al pasar el mouse, muestra info para todos los puntos en esa x.
                template="plotly_white",    # Tema de color claro.
                height=500,
                margin=dict(l=40, r=40, t=40, b=40)  # Márgenes.
            )
            # Mostrar el gráfico en Streamlit.
            st.plotly_chart(fig, use_container_width=True)

            # Sección desplegable para ver la tabla de puntos evaluados.
            with st.expander("Ver tabla de puntos evaluados"):
                max_rows = 100
                # Si hay demasiados puntos, se toma una muestra para no saturar la tabla.
                if len(result.x_values) > max_rows:
                    step = len(result.x_values) // max_rows  # Cada 'step' puntos se muestra uno.
                    indices = slice(None, None, step)        # Crear un slice para tomar cada 'step' elementos.
                    x_sample = np.array(result.x_values)[indices].tolist()
                    y_sample = np.array(result.y_values)[indices].tolist()
                    st.info(f"Mostrando {len(x_sample)} de {len(result.x_values)} puntos (cada {step} puntos).")
                else:
                    x_sample = result.x_values
                    y_sample = result.y_values
                    st.info(f"Mostrando todos los {len(x_sample)} puntos.")

                # Construir un DataFrame de pandas para mostrar en tabla.
                import pandas as pd
                df = pd.DataFrame({
                    "x": x_sample,
                    "f(x)": y_sample
                })
                st.dataframe(df, use_container_width=True)

        # Pestañas futuras (aún no implementadas).
        with tab2:
            st.info("La Fase 2 implementara el analisis de limites laterales y en el infinito.")
        with tab3:
            st.info("La Fase 3 implementara la diferenciacion numerica y simbolica.")
        with tab4:
            st.info("La Fase 4 implementara metodos de optimizacion (raices, maximos/minimos).")

    except InvalidExpressionError as e:
        # Si la expresión no es válida, se captura la excepción y se muestra un mensaje de error.
        st.error(f"Error en la expresion: {e}")
        st.stop()
    except Exception as e:
        # Cualquier otra excepción inesperada.
        st.error(f"Error inesperado: {e}")
        st.stop()

    # --- Sección informativa sobre la arquitectura y su relación con el cálculo diferencial ---
    with st.expander("Acerca de la arquitectura y su relación con el Calculo Diferencial"):
        st.markdown("""
        **Arquitectura Hexagonal y DDD**:
        - El **Dominio** (carpeta `domain`) contiene las entidades matematicas puras (funcion, dominio, puntos).
          No depende de librerias externas.
        - Los **Casos de Uso** (`application`) orquestan la evaluacion, separando la logica de negocio de la presentacion.
        - Los **Adaptadores** (`infrastructure`) implementan las operaciones concretas (SymPy para evaluacion simbolica,
          Streamlit/Plotly para la interfaz).

        **Calculo Diferencial en esta Fase 1**:
        - Visualizacion de funciones en un dominio continuo, fundamental para entender limites y continuidad.
        - Evaluacion numerica de funciones.
        - La representacion LaTeX facilita la comprension simbolica de las funciones.
        """)

# Este bloque permite ejecutar el script directamente para pruebas.
if __name__ == "__main__":
    main()