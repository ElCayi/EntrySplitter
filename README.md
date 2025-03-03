# Calculadora de Riesgo v4.0

Este programa ayuda a calcular la gestión del riesgo en operaciones de trading, incluyendo el cálculo automático del apalancamiento basado en el porcentaje de riesgo y el rango de precios esperado. El programa permite al usuario configurar ajustes, ingresar valores de capital y riesgo, y calcular el apalancamiento y el riesgo para diferentes escenarios.

## Resumen

El programa proporciona una interfaz simple e interactiva con un menú principal donde el usuario puede elegir entre:

1. Usar la configuración actual para el cálculo de riesgo.
2. Modificar la configuración de las entradas.
3. Salir del programa.

El programa calcula el riesgo basado en un capital total definido por el usuario, el porcentaje de riesgo máximo y los ajustes de apalancamiento.

## Componentes Clave

### 1. **Archivo de Configuración (`config_manager.py`)**

El programa depende de un archivo de configuración para gestionar las entradas. Estas entradas son esenciales para el proceso de cálculo del riesgo. El archivo proporciona un diccionario con información de cada entrada, incluyendo pesos y niveles de stop-loss.

- **Entradas**: Una lista de entradas que el usuario puede configurar, cada una con las siguientes claves:
  - **peso**: Define el peso relativo de la entrada en el cálculo.
  - **stop_loss**: El valor de stop-loss asociado con la entrada.

El archivo de configuración esperado debe tener una estructura similar a la siguiente (ejemplo):

```json
{
  "entradas": [
    {"peso": 0.4, "stop_loss": 0.05},
    {"peso": 0.6, "stop_loss": 0.10}
  ]
}
```

- **`entradas`**: Una lista que contiene varias entradas. Cada entrada tiene un **peso** y un **stop_loss**.

#### Propósito de los Valores de Configuración:
- **Peso**: Define cuánta importancia tiene cada entrada en el cálculo total del riesgo.
- **Stop Loss**: Especifica el valor de stop-loss que se utilizará en el cálculo para determinar la exposición al riesgo de cada entrada.

### 2. **Flujo Principal del Programa**

#### **Navegación del Menú**:
Al ejecutar el programa, el usuario verá un menú principal con las siguientes opciones:

1. **Usar esta configuración**: Usará la configuración actual para el cálculo de riesgo.
2. **Modificar configuración**: Permite al usuario modificar las entradas (peso y stop-loss) antes de continuar.
3. **Volver**: Regresa al inicio del programa.

#### **Cálculo del Riesgo**:
Después de seleccionar o modificar la configuración, se le pedirá al usuario que ingrese:
- **Capital Total (USD)**: El monto total de capital que el usuario está dispuesto a invertir.
- **Riesgo Máximo en Porcentaje**: El porcentaje del capital que está dispuesto a arriesgar.

El programa luego ofrecerá dos opciones para calcular el apalancamiento:
1. **Cálculo Automático de Apalancamiento**: Si se selecciona esta opción, el programa pedirá el **precio mínimo esperado** y el **precio máximo esperado** para calcular automáticamente el apalancamiento basado en la diferencia entre los precios.
   
2. **Apalancamiento Manual**: Si se elige el apalancamiento manual, el usuario debe ingresar el apalancamiento deseado.

El sistema también emitirá una advertencia si el apalancamiento ingresado excede de 50x.

#### **Cálculo de Apalancamiento**:
Para el cálculo automático de apalancamiento, el programa utiliza la siguiente fórmula:

```
apalancamiento = (riesgo_maximo_porcentaje * suma_pesos) / (suma_pesos_stop_loss * rango_precio)
```

Donde:
- **riesgo_maximo_porcentaje**: El porcentaje de riesgo máximo ingresado por el usuario.
- **suma_pesos**: El peso total de todas las entradas.
- **suma_pesos_stop_loss**: La suma del producto de cada entrada con su stop-loss.
- **rango_precio**: La diferencia entre el precio máximo y el precio mínimo esperado.

### 3. **Manejo de Errores**

El programa incluye manejo de errores para asegurar que la entrada del usuario sea válida. Por ejemplo:
- Si el rango de precios es menor o igual a cero, se muestra un mensaje de error.
- Si la suma del producto de pesos y stop-loss es cero, se muestra una advertencia.

Si el usuario decide cancelar o volver al menú principal en cualquier momento, el programa permite hacerlo.

### 4. **Salir y Repetir**

Después de completar un cálculo, se le preguntará al usuario si desea realizar otro cálculo o salir del programa.

---

## Ejecución del Programa

Para ejecutar el programa, simplemente ejecuta el archivo `main.py`:

```bash
python main.py
```

El programa guiará al usuario a través de los pasos de manera interactiva, solicitando las entradas necesarias según los ajustes de configuración.

---

## Formato Esperado del Archivo de Configuración

El archivo de configuración (`config.json`) debe contener una lista de "entradas", donde cada entrada tiene un `peso` y un `stop_loss`. Ejemplo:

```json
{
  "entradas": [
    {
      "peso": 0.5,
      "stop_loss": 0.05
    },
    {
      "peso": 0.3,
      "stop_loss": 0.10
    },
    {
      "peso": 0.2,
      "stop_loss": 0.15
    }
  ]
}
```

### Explicación de los Valores de Configuración:
- **peso**: El peso de cada entrada (cuánto capital se asigna a cada operación). La suma de todos los pesos debería ser generalmente igual a 1 (100% de tu capital).
- **stop_loss**: Este valor indica el nivel de stop-loss para cada operación, que se utilizará en el cálculo del riesgo de cada entrada. El valor de stop-loss se expresa como un porcentaje (por ejemplo, 0.05 para un 5%).

---

## Conclusión

Este programa es una herramienta simple pero efectiva para calcular la gestión del riesgo en escenarios de trading. Al permitir que los usuarios ingresen su capital, porcentaje de riesgo y apalancamiento deseado, puede ayudar a los traders a tomar decisiones más informadas basadas en su tolerancia al riesgo y expectativas del mercado.

# Notas
Entorno de trabajo (ANACONDA):CCF