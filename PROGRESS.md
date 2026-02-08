# Progreso del Proyecto

## Estado General
- **Fecha ultima actualizacion:** 2026-02-08
- **Branch:** master
- **Commits pusheados:** 2 commits en GitHub (Ag1l1ty/prompt-eng-interactive-tutorial)

## Tareas

### 1. Fork y reestructurar el repositorio
- **Estado:** HECHO
- **Detalle:** Archivos movidos de `Anthropic 1P/` a raiz. Nombres en espanol. `AmazonBedrock/` eliminado. `hints.py` consolidado.

### 2. Crear Capitulo 10: Pensamiento Extendido
- **Estado:** HECHO
- **Archivo:** `10_Pensamiento_Extendido.ipynb`
- **Contenido:** Extended thinking API, budget_tokens, comparaciones, 3 ejercicios (10.1, 10.2, 10.3)

### 3. Crear Capitulo 11: System Prompts Avanzados
- **Estado:** HECHO
- **Archivo:** `11_System_Prompts_Avanzados.ipynb`
- **Contenido:** Multi-seccion XML, personas, guardrails, formato JSON, 3 ejercicios (11.1, 11.2, 11.3)

### 4. Escribir README.md en espanol
- **Estado:** HECHO
- **Archivo:** `README.md`

### 5. Actualizar modelos a Claude Opus 4.6
- **Estado:** HECHO
- **Detalle:** Todos los notebooks usan MODEL_NAME definido en notebook 00 como `claude-opus-4-6`. Verificado en todos los archivos.

### 6. Corregir bugs conocidos
- **Estado:** HECHO
- **Bugs corregidos:**
  - [x] #56 - hints module not found (sys.path fix)
  - [x] #61 - Modelo deprecado en 12.2 Tool Use (resuelto via MODEL_NAME + reescritura completa)
  - [x] #48 - Cap 8 hallucination techniques conflated (explicacion reescrita)
  - [x] #11 - Typo "handilgj" en 12.2 (eliminado en reescritura)
  - [x] #10 - f-string missing en Cap 9 (f-prefix agregado)
  - [x] #43 - Link 404 en Cap 1 (URL actualizada)
  - [x] #2 - LICENSE file agregado

### 7. Traducir todos los notebooks a espanol
- **Estado:** HECHO
- **Verificacion automatizada:** Todos los notebooks contienen markdown en espanol, comentarios en espanol, prompts en ingles (intencionalmente).
  - [x] 00_Tutorial_Como_Empezar
  - [x] 01_Estructura_Basica_de_Prompts
  - [x] 02_Ser_Claro_y_Directo
  - [x] 03_Asignacion_de_Roles
  - [x] 04_Separar_Datos_de_Instrucciones
  - [x] 05_Formato_de_Output_y_Hablar_por_Claude
  - [x] 06_Precognicion_Pensar_Paso_a_Paso
  - [x] 07_Uso_de_Ejemplos_Few_Shot
  - [x] 08_Evitar_Alucinaciones
  - [x] 09_Prompts_Complejos_desde_Cero
  - [x] 10_Pensamiento_Extendido (creado en espanol)
  - [x] 11_System_Prompts_Avanzados (creado en espanol)
  - [x] 12.1_Apendice_Encadenamiento_de_Prompts
  - [x] 12.2_Apendice_Uso_de_Herramientas (reescrito en espanol)
  - [x] 12.3_Apendice_Busqueda_y_Recuperacion

### 8. Modernizar apendice de Tool Use (12.2)
- **Estado:** HECHO
- **Detalle:** Notebook completamente reescrito para usar la API moderna nativa de Anthropic:
  - Herramientas definidas como diccionarios Python con JSON Schema (no XML)
  - Parametro `tools` nativo en `client.messages.create()` (no system prompt)
  - Manejo estructurado de `ToolUseBlock` (no parsing XML manual)
  - Bucle agentico completo con `stop_reason == "tool_use"` (no stop_sequences hack)
  - Ejercicio actualizado para usar formato moderno
  - Hint en hints.py actualizado al formato moderno
