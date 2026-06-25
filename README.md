# ⚙️ Autómatas y Lenguajes (AUTLEN)

Este repositorio contiene el código y la resolución de las prácticas de la asignatura de **Autómatas y Lenguajes** de la Universidad Autónoma de Madrid (UAM) correspondientes al curso 2025-26.

El proyecto aborda el diseño e implementación de sistemas reconocedores de lenguajes formales, evolucionando desde expresiones regulares y autómatas finitos hasta analizadores sintácticos y semánticos complejos. Todo el entorno está desarrollado en **Python** empleando el paradigma de Programación Orientada a Objetos, ideal para entornos de desarrollo como Visual Studio Code.

## 🛠️ Tecnologías y Librerías

* **Lenguaje:** Python 3.
* **Módulos Estándar:** `re` (Regular Expression Operations), `unittest` (para validación de código).
* **Herramientas Externas:** `ply` (Python Lex-Yacc) para la construcción de analizadores léxicos y sintácticos.

## 🚀 Estructura del Repositorio

El proyecto está dividido en tres prácticas incrementales que reflejan el proceso teórico y práctico de procesamiento de lenguajes:

### 1. Expresiones Regulares (Práctica 1)

Diseño de expresiones regulares para el reconocimiento, filtrado y extracción de patrones.

* Uso intensivo del módulo `re` de Python.
* Implementación de expresiones para validar cadenas binarias, correos institucionales y rangos numéricos.
* Uso de captura de grupos para el procesado estructurado de datos (ej. extracción de día/mes/año de una fecha y separación de octetos en direcciones IPv4).

### 2. Autómatas Finitos (Práctica 2)

Construcción de una arquitectura completa para la simulación y operación de autómatas.

* **Simulación:** Creación de la clase `FiniteAutomaton` para procesar y evaluar la aceptación de cadenas.
* **Conversión de Lenguajes:** Implementación del algoritmo para convertir Expresiones Regulares abstractas en Autómatas Finitos No Deterministas (AFnD) mediante la clase `REParser`.
* **Determinismo:** Desarrollo del algoritmo de transformación de AFnD a AFD (Autómata Finito Determinista), resolviendo el manejo de transiciones lambda.
* **Optimización:** Implementación del algoritmo de minimización de AFD, depurando estados equivalentes e inaccesibles.

### 3. Análisis Sintáctico y Semántico (Práctica 3)

Desarrollo de parsers descendentes y ascendentes para la evaluación y traducción de lenguajes.

* **Analizador LL(1) Descendente:** Implementación algorítmica para el cálculo automático de los conjuntos PRIMERO (First) y SIGUIENTE (Follow). Construcción de la tabla de análisis LL(1) y generación de árboles de derivación.
* **Analizador LALR Ascendente:** Integración de la herramienta `ply` para la evaluación de Gramáticas Independientes del Contexto (GIC).
* **Análisis Semántico (Gramática de Atributos):** Inyección de reglas semánticas para calcular valores en tiempo real, aplicado específicamente a la validación estructural y traducción matemática de números romanos a números arábigos.

## ⚙️ Ejecución y Entorno de Pruebas

El código fuente está preparado para ejecutarse y testearse directamente. Para la práctica 3, asegúrate de tener instalada la dependencia Lex-Yacc de Python:

```bash
pip install ply

```

El repositorio incluye un conjunto de pruebas unitarias (`test_*.py`) basadas en el módulo estándar `unittest` para garantizar la precisión de los algoritmos. Se pueden lanzar de la siguiente forma:

```bash
# Ejemplo de ejecución de tests para la Práctica 2
python -m unittest test_evaluator.py
python -m unittest test_to_deterministic.py

```

## 👨‍💻 Autor

* **Juan Herrero Pérez** - Estudiante de Ingeniería Informática (Universidad Autónoma de Madrid)
