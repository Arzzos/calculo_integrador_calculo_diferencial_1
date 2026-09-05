# Motor Interactivo de Análisis de Funciones

## Proyecto Integrador - Cálculo Diferencial

Este proyecto es una aplicación interactiva desarrollada con Python que permite graficar y analizar funciones matemáticas.

La aplicación utiliza una arquitectura hexagonal (puertos y adaptadores) combinada con Domain-Driven Design (DDD)..

---

## Tabla de Contenidos

1. [Características principales](#caracteristicas-principales)
2. [Requisitos e instalación](#requisitos-e-instalacion)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Cómo usar la aplicación](#como-usar-la-aplicacion)
   - [Ejecución local](#ejecucion-local)
   - [Interfaz de usuario](#interfaz-de-usuario)
5. [Expresiones válidas y símbolos aceptados](#expresiones-validas-y-simbolos-aceptados)
6. [Ejemplos de uso](#ejemplos-de-uso)
7. [Arquitectura y patrones](#arquitectura-y-patrones)
8. [Pruebas unitarias](#pruebas-unitarias)
9. [Contribuir al proyecto](#contribuir-al-proyecto)
10. [Licencia](#licencia)

---

## Características principales

- **Graficación interactiva:** Genera gráficos dinámicos con Plotly, permitiendo explorar la función de manera visual.
- **Evaluación numérica:** Evalúa la función en un dominio definido por el usuario con un número ajustable de puntos.
- **Soporte simbólico:** Utiliza SymPy para validar expresiones y generar representaciones LaTeX.
- **Arquitectura extensible:** Diseñada para añadir nuevas funcionalidades (límites, derivadas, optimización) en fases posteriores.
- **Interfaz amigable:** Construida con Streamlit, ofrece controles intuitivos y visualización clara.

---

## Requisitos e instalación

### Requisitos previos

- Python 3.8 o superior.
- pip (gestor de paquetes de Python).

### Pasos para instalar

1. Clonar el repositorio o descargar los archivos del proyecto.
   ```bash
   git clone https://github.com/Arzzos/calculo_integrador_calculo_diferencial_1.git
   ```
2. Abrir una terminal en la carpeta raíz del proyecto.
3. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```
4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Estructura del proyecto

El proyecto sigue una arquitectura hexagonal que separa las capas:

- `src/domain/`: Contiene la base del proyecto (entidades, objetos de valor, excepciones y puertos).
- `src/application/`: Orquesta los casos de uso utilizando los puertos del dominio. Incluye DTOs para transferencia de datos.
- `src/infrastructure/`: Implementa los adaptadores concretos (SymPy para el motor matemático, Streamlit para la interfaz de usuario).
- `app.py`: Punto de entrada que inicializa la aplicación.
- `test_domain.py`: Pruebas unitarias para las clases del dominio.
- `requirements.txt`: Lista de dependencias.

---

## Cómo usar la aplicación

### Ejecución local

Desde la carpeta raíz del proyecto, ejecutar:

```bash
streamlit run app.py
```

Esto abrirá automáticamente la aplicación en el navegador predeterminado.

### Interfaz de usuario

La interfaz se divide en:

- **Barra lateral:** Permite ingresar la expresión matemática ($f(x)$), definir el dominio ($x_{\text{min}}$, $x_{\text{max}}$) y ajustar la resolución (Número de puntos).
- **Área principal:** Muestra la función en formato LaTeX, la gráfica interactiva y una tabla de puntos evaluados (colapsable).
- **Pestañas:** Actualmente solo está activa la pestaña "Explorador de Funciones"; las demás (Límites, Derivadas, Optimización) están reservadas para fases futuras.
- **Sección informativa:** Despliega una explicación de la arquitectura y su relación con el cálculo diferencial.

Cada cambio en los controles actualiza automáticamente la gráfica y la tabla.

---

## Expresiones válidas y símbolos aceptados

La aplicación acepta expresiones escritas en notación estándar de Python, utilizando el operador `**` para potencias. Las funciones matemáticas disponibles son:

- **Operadores:** `+`, `-`, `*`, `/`, `**` (potencia).
- **Funciones trigonométricas:** `sin(x)`, `cos(x)`, `tan(x)`.
- **Funciones exponenciales y logarítmicas:** `exp(x)`, `log(x)` (logaritmo natural), `log10(x)` (logaritmo base 10).
- **Raíces:** `sqrt(x)`.
- **Valor absoluto:** `abs(x)`.
- **Constantes:** `pi` ($\pi$), `e` (número de Euler).
- **Otras:** `sinh`, `cosh`, `tanh`, `asin`, `acos`, `atan`, etc., siempre que SymPy las reconozca.

### Ejemplos de expresiones válidas:

- `x**2 - 3*x + 2`
- `sin(x) + cos(2*x)`
- `exp(-x**2)`
- `log(x) / sqrt(x)`
- `abs(x-2)`
- `x**3 + pi*x - e`

> **Nota:** La variable independiente debe ser siempre `x` (minúscula). No se permiten otras variables.

---

## Ejemplos de uso

1. **Función polinomial:** `x**3 - 3*x + 2`
   - Dominio: `[-5, 5]`
   - Puntos: `200`
   - Resultado: Gráfica con raíces y puntos extremos visibles.

2. **Función senoidal:** `sin(x) + 0.5*sin(3*x)`
   - Dominio: `[-2*pi, 2*pi]`
   - Puntos: `300`
   - Resultado: Curva con armónicos.

3. **Función exponencial:** `exp(-x**2)`
   - Dominio: `[-3, 3]`
   - Puntos: `150`
   - Resultado: Campana de Gauss.

4. **Función racional:** `1/(x**2 + 1)`
   - Dominio: `[-5, 5]`
   - Puntos: `200`
   - Resultado: Curva con asíntota horizontal en 0.

---

## Arquitectura y patrones

### Arquitectura Hexagonal (Puertos y Adaptadores)

- **Puertos:** Interfaces definidas en el dominio (ej. `EvaluatorPort`) que declaran qué operaciones necesita el dominio.
- **Adaptadores:** Implementaciones concretas de esos puertos en la infraestructura (ej. `SympyEvaluatorAdapter`), que usan librerías externas (SymPy) y pueden ser reemplazadas.
- **Caso de uso:** Orquesta la lógica (ej. `EvaluateFunctionUseCase`) sin conocer los detalles de implementación del adaptador.

### Domain-Driven Design (DDD)

- **Entidades:** Objetos con identidad y ciclo de vida (ej. `FunctionModel`).
- **Objetos de valor:** Objetos inmutables que se definen por sus atributos (ej. `Expression`, `Interval`).

### Beneficios

- **Mantenibilidad:** Cambiar el motor matemático (por ejemplo, a SageMath) solo requiere implementar un nuevo adaptador.
- **Testabilidad:** Los casos de uso pueden probarse con adaptadores falsos (mocks).
- **Colaboración:** Diferentes equipos pueden trabajar en las capas de dominio, aplicación e infraestructura de forma paralela.

---

## Pruebas unitarias

El archivo `test_domain.py` contiene pruebas para las clases del dominio. Para ejecutarlas, instalar `pytest` (si no está en `requirements.txt`, agregarlo) y correr:

```bash
python -m pytest tests/test_domain.py -v
```

Se espera que todas las pruebas pasen. Las pruebas verifican la creación de objetos, validaciones y excepciones.

---

## Contribuir al proyecto

Si deseas contribuir, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una rama con tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y asegúrate de que las pruebas pasen.
4. Envía un pull request describiendo los cambios.

---
*Última actualización: 05/09/2026*