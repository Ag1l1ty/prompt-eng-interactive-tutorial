# Progreso del Proyecto

## Estado General
- **Fecha ultima actualizacion:** 2026-02-09
- **Branch:** master
- **Web App:** https://prompt-eng-interactive-tutorial-2uvqtvg3te5ugk5phb35kq.streamlit.app
- **Estado:** COMPLETO - todas las tareas finalizadas y en produccion.

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
- **Detalle:** Todos los notebooks usan MODEL_NAME definido en notebook 00 como `claude-opus-4-6`.

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
- **Verificacion:** Todos los 15 notebooks traducidos. Markdown en espanol, prompts en ingles.
  - [x] 00 a 09 (originales traducidos)
  - [x] 10, 11 (creados en espanol)
  - [x] 12.1, 12.2 (traducidos/reescritos), 12.3 (traducido)

### 8. Modernizar apendice de Tool Use (12.2)
- **Estado:** HECHO
- **Detalle:** Reescrito para API moderna: JSON Schema, parametro `tools` nativo, `ToolUseBlock`, bucle agentico.

### 9. Streamlit Web App (v1)
- **Estado:** HECHO (reemplazada por v2 en tarea 10)
- **Detalle:** Version inicial con 14 paginas y 26 ejercicios. Prompts en ingles.

### 10. Reestructuracion a 10 capitulos (v2)
- **Estado:** HECHO
- **Deploy:** Streamlit Cloud (auto-deploy desde master)
- **URL:** https://prompt-eng-interactive-tutorial-2uvqtvg3te5ugk5phb35kq.streamlit.app
- **Cambios clave:**
  - Reducido de 14 a 10 capitulos (eliminados: API basics, roles, CoT, encadenamiento)
  - Todos los prompts y ejemplos traducidos a espanol
  - Eliminado patron `print(get_completion(PROMPT))` - contenido narrativo, no codigo
  - Grading bilingue (regex acepta respuestas en espanol o ingles)
  - 24 ejercicios calificados (antes 26)
  - Emails de prueba (Cap 4) traducidos a espanol
- **Capitulos eliminados/absorbidos:**
  - Cap 1 original (Estructura Basica/API) -> eliminado
  - Cap 3 original (Roles) -> absorbido en Cap 8 (System Prompts)
  - Cap 6 original (CoT/Precognicion) -> absorbido en Cap 7 (Extended Thinking)
  - Cap 12.1 (Encadenamiento) -> absorbido como bonus en Cap 6 (Prompts Complejos)
- **Archivos actuales (19):**
  - `streamlit_app/app.py` - Pagina de inicio (10 capitulos)
  - `streamlit_app/requirements.txt` - Dependencias
  - `streamlit_app/.streamlit/config.toml` - Tema
  - `streamlit_app/utils/api.py` - API wrapper (normal + thinking + tools)
  - `streamlit_app/utils/components.py` - Componentes UI (total=24)
  - `streamlit_app/utils/grading.py` - 24 funciones de calificacion bilingues
  - `streamlit_app/utils/data.py` - Documentos de referencia (49K)
  - `streamlit_app/pages/01-10` - 10 paginas interactivas
- **Verificacion:**
  - [x] Todas las paginas compilan sin errores de sintaxis
  - [x] 23/23 tests de calificacion pasan (+ 2 abiertos sin grading)
  - [x] Todas las importaciones resuelven correctamente
  - [x] App arranca sin errores (`streamlit run streamlit_app/app.py`)
  - [x] 10/10 paginas retornan HTTP 200
  - [x] Deploy exitoso en Streamlit Cloud
