# Progreso del Proyecto

## Estado General
- **Fecha ultima actualizacion:** 2026-02-08
- **Branch:** master
- **Commits pusheados:** NINGUNO - todo el trabajo esta local

## Tareas

### 1. Fork y reestructurar el repositorio
- **Estado:** HECHO (local, sin commit)
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
- **Estado:** EN PROGRESO
- **Que falta:** Verificar que TODOS los notebooks usen `claude-opus-4-6`. El notebook 00 define MODEL_NAME. Revisar especialmente 12.2 (Tool Use) que usaba modelo deprecado.

### 6. Corregir bugs conocidos
- **Estado:** EN PROGRESO
- **Bugs por verificar:**
  - [ ] #61 - Modelo deprecado en 12.2 Tool Use
  - [ ] #48 - Cap 8 hallucination techniques conflated
  - [ ] #11 - Typo "handilgj" en 12.2
  - [ ] #10 - f-string missing en Cap 9
  - [ ] #43 - Link 404 en Cap 1
- **Bugs ya corregidos:**
  - [x] #56 - hints module not found (sys.path fix)
  - [x] #2 - LICENSE file agregado

### 7. Traducir todos los notebooks a espanol
- **Estado:** EN PROGRESO
- **Notebooks por verificar completitud de traduccion:**
  - [ ] 00_Tutorial_Como_Empezar
  - [ ] 01_Estructura_Basica_de_Prompts
  - [ ] 02_Ser_Claro_y_Directo
  - [ ] 03_Asignacion_de_Roles
  - [ ] 04_Separar_Datos_de_Instrucciones
  - [ ] 05_Formato_de_Output_y_Hablar_por_Claude
  - [ ] 06_Precognicion_Pensar_Paso_a_Paso
  - [ ] 07_Uso_de_Ejemplos_Few_Shot
  - [ ] 08_Evitar_Alucinaciones
  - [ ] 09_Prompts_Complejos_desde_Cero
  - [x] 10_Pensamiento_Extendido (creado en espanol)
  - [x] 11_System_Prompts_Avanzados (creado en espanol)
  - [ ] 12.1_Apendice_Encadenamiento_de_Prompts
  - [ ] 12.2_Apendice_Uso_de_Herramientas
  - [ ] 12.3_Apendice_Busqueda_y_Recuperacion

### 8. Modernizar apendice de Tool Use (12.2)
- **Estado:** PENDIENTE
- **Bloqueado por:** Tareas 5 y 6
- **Detalle:** Actualizar a API moderna de tool_use de Anthropic
