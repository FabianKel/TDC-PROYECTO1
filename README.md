# Proyecto: Procesamiento y Simulación de Autómatas

Este proyecto se enfoca en la construcción y simulación de Autómatas Finitos No Deterministas (AFN) y Deterministas (AFD) a partir de expresiones regulares, así como en la minimización de AFDs.

## Descripción

El programa toma una expresión regular `r` y una cadena `w`, y sigue un flujo de procesamiento que incluye varios pasos:

1. **Formato de la Expresión Regular** (`format_regex.py`):
   - En este programa, se utiliza un formato específico para interpretar y procesar las expresiones regulares. A continuación, se describen las reglas y convenciones utilizadas:

    -  **Concatenación Implícita**:
        - En la expresión regular, la concatenación entre dos caracteres es implícita. Es decir, cuando dos caracteres están juntos, se asume que deben ser concatenados.
        - Ejemplo: `ab` se interpreta como `a` concatenado con `b`.

    -   **Representación del Conjunto Vacío**:
        - El conjunto vacío se representa por el símbolo `ε`.
        - Este símbolo se utiliza para denotar una cadena vacía o la ausencia de un valor en una expresión.

    - **Operador de Concatenación**:
        - Aunque la concatenación es implícita en la expresión inicial, se toma en cuenta el operador `•` para denotar la concatenación para el proceso de Shunting Yard y la creación del Árbol Sintáctico.
        - Ejemplo: `ab•` en postfix es equivalente a `ab` en infix, ambos representan la concatenación de `a` y `b`.
        - El punto normal `.` es tomado en cuenta como un caracter literal.

    - **Agrupación y Alternativas**:
        - El programa permite agrupar conjuntos de caracteres y definir alternativas usando corchetes `[]`.
        - Los corchetes se utilizan para agrupar opciones que están separadas por el operador OR (`|`).
        - Ejemplo: `[ae03]` se interpreta como `(a|e|0|3)`, donde la expresión acepta cualquiera de los caracteres `a`, `e`, `0` o `3`.

    - **Escape de Caracteres Especiales**:
        - El símbolo de backslash `\` se utiliza para escapar caracteres especiales y tratarlos como literales.
        - Por ejemplo, `\(` representa un paréntesis literal `(` en lugar de un signo de agrupación.
        - Esto permite incluir caracteres especiales en la expresión regular sin que se interpreten con su significado habitual.

    - **Otros Operadores Comunes**:
        - `+`: Denota una o más repeticiones del elemento precedente.
            - Ejemplo: `a+` se traduce a `aa*`.
        - `?`: Denota la presencia opcional del elemento precedente, equivalente a `0` o `1` ocurrencias.
            - Ejemplo: `1?` se traduce a `1|ε`.

    Estas reglas y convenciones permiten que las expresiones regulares sean interpretadas de manera consistente por el programa, facilitando su conversión y el posterior procesamiento en los autómatas correspondientes.

2. **Conversión a Postfix** (`infix2postfix.py`):
   - La expresión regular formateada se convierte a notación postfix con el algoritmo de Shunting Yard.

3. **Construcción del Árbol Sintáctico** (`tree.py`):
   - Utilizando la biblioteca `nltk`, se construye un árbol sintáctico a partir de la notación postfix.

4. **Construcción del AFN con el Algoritmo de Thompson** (`Thompson_nfa.py`):
   - A partir del árbol sintáctico, se genera un Autómata Finito No Determinista (AFN) utilizando el algoritmo de Thompson.
   - El AFN se grafica utilizando `Graphviz`.

5. **Conversión del AFN a AFD** (`afn_to_afd.py`):
   - El AFN generado se convierte en un Autómata Finito Determinista (AFD) utilizando el algoritmo de construcción de subconjuntos.
   - El AFD también se grafica utilizando `Graphviz`.

6. **Minimización del AFD** (`afd_to_minimized.py`):
   - El AFD se minimiza utilizando el método de particiones.

7. **Simulación y Verificación** (`utils.py`):
   - Se implementa la simulación para verificar si la cadena `w` es aceptada por el AFN, AFD y AFD minimizado.

## Ejemplo
Para la expresión `(a*|b*)+`
1. **Format Regex**: `(a*|b*)•(a*|b*)*`
2. **Postfix**: `a*b*|a*b*|*•`
3. **Árbol Sintáctico**: 
4. **AFN**: 
5. **AFD**:
6. **AFD Minimizado**:
7. **Simulación**: Para la cadena `aba`:
```bash
La cadena 'aba' SI es aceptada por el AFN
La cadena 'aba' SI es aceptada por el AFD
La cadena 'aba' SI es aceptada por el AFD Minimizado
```


## Archivos Principales

- `format_regex.py`: Formatea y traduce la expresión regular.
- `infix2postfix.py`: Convierte la expresión regular a notación postfix.
- `tree.py`: Construye el árbol sintáctico usando `nltk`.
- `Thompson_nfa.py`: Construye el AFN con el algoritmo de Thompson y lo grafica.
- `afn_to_afd.py`: Convierte el AFN a AFD y lo grafica.
- `afd_to_minimized.py`: Minimiza el AFD.
- `utils.py`: Integra todos los métodos, lee archivos de entrada, y verifica la aceptación de la cadena `w`.

## Ejecución

Para ejecutar el programa, asegúrate de tener instaladas las dependencias necesarias. Luego, puedes utilizar `main.py` para procesar un conjunto de expresiones regulares y una cadena `w`.

### Pasos para ejecutar el programa:

1. **Instalar las Dependencias**:
   - Asegúrate de tener instalados Python 3.x, `nltk` y `Graphviz`.

2. **Ejecutar el Programa**:
   - Ejecuta `main.py`, que se encargará de leer la expresión regular desde `regex.txt`, procesarla a través de los diferentes módulos y verificar si la cadena `w` es aceptada por los autómatas generados.

4. **Verificar la Salida**:
   - El programa generará gráficos de los autómatas en cada etapa (AFN, AFD, AFD minimizado) y mostrará si la cadena `w` es aceptada por cada uno de ellos.

## Entrada

- `regex.txt`: Archivo de texto que contiene las expresiones regulares a procesar.

## Salida

El programa generará gráficos de los autómatas y verificará si la cadena `w` es aceptada por cada uno de ellos. Guardando las imágenes de las Autómatas en las carpetas [AFNs](/AFNAFNs/) y [AFDs](/AFDs/) e imprimiendo en la consola los resultados de la cadena `w` en cada una.


## Dependencias

- `nltk`
- `Graphviz`
- `Python 3.x`

## Contacto
Programa Hecho por:
- [Mónica Salvatierra](https://github.com/alee2602) 22249
- [Derek Arreaga](https://github.com/FabianKel) 22537