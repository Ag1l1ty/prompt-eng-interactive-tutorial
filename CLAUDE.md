# CLAUDE.md - Contexto del Proyecto

## Resumen del Proyecto

Fork en espanol del tutorial interactivo de ingenieria de prompts de Anthropic, con web app Streamlit.
- **Repo original:** `anthropics/prompt-eng-interactive-tutorial`
- **Repo destino:** `Ag1l1ty/prompt-eng-interactive-tutorial`
- **Web App:** https://prompt-eng-interactive-tutorial-2uvqtvg3te5ugk5phb35kq.streamlit.app
- **Estado:** COMPLETO - todas las tareas finalizadas y en produccion.

## Estado del Repositorio

- **Directorio local:** `/Users/agilitychanges/prompt-eng-interactive-tutorial`
- **Remote `origin`:** `https://github.com/Ag1l1ty/prompt-eng-interactive-tutorial.git`
- **Remote `upstream`:** `https://github.com/anthropics/prompt-eng-interactive-tutorial.git`
- **Branch:** `master`
- **Git config:** `Ag1l1ty` / `229850407+Ag1l1ty@users.noreply.github.com`
- **Deploy:** Streamlit Cloud, apunta a `streamlit_app/app.py` en branch `master`

## Estructura de Archivos

```
prompt-eng-interactive-tutorial/
├── .gitignore
├── LICENSE
├── README.md                               # Instrucciones en espanol
├── requirements.txt                        # Para Jupyter notebooks
├── hints.py                                # Pistas para ejercicios (notebooks)
├── CLAUDE.md                               # Este archivo - contexto del proyecto
├── PROGRESS.md                             # Historial de tareas completadas
│
├── 00_Tutorial_Como_Empezar.ipynb          # Setup inicial (API key, modelo)
├── 01_Estructura_Basica_de_Prompts.ipynb
├── 02_Ser_Claro_y_Directo.ipynb
├── 03_Asignacion_de_Roles.ipynb
├── 04_Separar_Datos_de_Instrucciones.ipynb
├── 05_Formato_de_Output_y_Hablar_por_Claude.ipynb
├── 06_Precognicion_Pensar_Paso_a_Paso.ipynb
├── 07_Uso_de_Ejemplos_Few_Shot.ipynb
├── 08_Evitar_Alucinaciones.ipynb
├── 09_Prompts_Complejos_desde_Cero.ipynb
├── 10_Pensamiento_Extendido.ipynb          # Capitulo nuevo
├── 11_System_Prompts_Avanzados.ipynb       # Capitulo nuevo
├── 12.1_Apendice_Encadenamiento_de_Prompts.ipynb
├── 12.2_Apendice_Uso_de_Herramientas.ipynb # Reescrito con API moderna
├── 12.3_Apendice_Busqueda_y_Recuperacion.ipynb
│
└── streamlit_app/                          # Web app interactiva
    ├── app.py                              # Pagina de inicio + API key + progreso
    ├── requirements.txt                    # streamlit>=1.29.0, anthropic>=0.39.0
    ├── .streamlit/config.toml              # Tema naranja personalizado
    ├── pages/                              # 14 capitulos (Streamlit multi-page)
    │   ├── 01_Estructura_Basica.py
    │   ├── 02_Ser_Claro_y_Directo.py
    │   ├── 03_Asignacion_de_Roles.py
    │   ├── 04_Separar_Datos.py
    │   ├── 05_Formato_Output.py
    │   ├── 06_Precognicion.py
    │   ├── 07_Few_Shot.py
    │   ├── 08_Evitar_Alucinaciones.py
    │   ├── 09_Prompts_Complejos.py
    │   ├── 10_Pensamiento_Extendido.py
    │   ├── 11_System_Prompts.py
    │   ├── 12_Encadenamiento.py
    │   ├── 13_Herramientas.py
    │   └── 14_RAG.py
    └── utils/
        ├── __init__.py
        ├── api.py                          # Claude API wrapper
        ├── components.py                   # UI reutilizable
        ├── grading.py                      # 26 funciones de calificacion
        └── data.py                         # Documentos de referencia (Cap 8-9)
```

---

## Arquitectura de la Web App (Streamlit)

### Punto de entrada
- `streamlit_app/app.py` - Home page con API key input en sidebar y tabla de contenidos
- Streamlit descubre automaticamente las paginas en `pages/` y las muestra en el menu lateral

### Session State
```python
st.session_state.api_key    # str - API key de Anthropic
st.session_state.completed  # set - IDs de ejercicios completados (ej: {"1.1", "2.3", "10.1"})
```

### utils/api.py - Funciones de la API de Claude
| Funcion | Uso | Parametros clave |
|---------|-----|------------------|
| `get_client()` | Crea client Anthropic desde session_state | - |
| `get_completion(prompt, system_prompt, prefill)` | Llamada estandar | temp=0.0, max_tokens=2000 |
| `get_completion_with_thinking(prompt, system_prompt, budget_tokens)` | Extended thinking (Cap 10) | max_tokens=16000, retorna (thinking, response) |
| `run_tool_loop(user_message, tools, available_functions, system_prompt)` | Bucle agentico (Cap 12.2) | max 5 iteraciones, retorna (text, tool_log) |

**Modelo:** `claude-opus-4-6` (hardcoded en `MODEL_NAME` variable)

### utils/components.py - Componentes UI reutilizables
| Componente | Descripcion |
|------------|-------------|
| `init_session()` | Inicializa session_state (api_key, completed) |
| `render_sidebar()` | Sidebar con API key, barra de progreso, link a GitHub |
| `render_lesson(content)` | Renderiza markdown de leccion |
| `render_exercise(exercise_id, title, instruction, hint, grade_fn, fields, prefill, system_prompt_default)` | Ejercicio completo con inputs, ejecucion, calificacion |
| `render_multi_test_exercise(exercise_id, title, instruction, hint, test_cases, grade_fn, prompt_template, prefill)` | Ejercicio con multiples casos de prueba (Cap 6-7) |
| `render_code_demo(prompt, system_prompt, label)` | Demo ejecutable en expander |

### utils/grading.py - Funciones de calificacion
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_1_1(text)` | 1.1 | Contiene "1", "2", "3" |
| `grade_1_2(text)` | 1.2 | Contiene "giggles" o "soo" |
| `grade_2_1(text)` | 2.1 | Contiene "hola" |
| `grade_2_2(text)` | 2.2 | Exactamente "Michael Jordan" |
| `grade_2_3(text)` | 2.3 | >= 800 palabras |
| `grade_3_1(text)` | 3.1 | Contiene "incorrect" o "not correct" |
| `grade_4_1(text)` | 4.1 | Contiene "pigs" y "haiku" |
| `grade_4_2(text)` | 4.2 | Contiene "brown" |
| `grade_4_3(text)` | 4.3 | Contiene "brown" |
| `grade_5_1(text)` | 5.1 | Contiene "Warrior" (case-sensitive) |
| `grade_5_2(text)` | 5.2 | Contiene "cat", `<haiku>`, >5 lineas |
| `grade_5_3(text)` | 5.3 | Contiene "tail", "cat", `<haiku>` |
| `grade_6_1(response, test_case)` | 6.1 | Categoria correcta formato "B) B..." |
| `grade_6_2(response, test_case)` | 6.2 | Categoria en `<answer>X</answer>` |
| `grade_7_1(response, test_case)` | 7.1 | Ultimo caracter = letra correcta |
| `grade_8_1(text)` | 8.1 | Contiene "Unfortunately"/"I don't" Y NO contiene "2022" |
| `grade_8_2(text)` | 8.2 | Contiene "49-fold" |
| `grade_10_1(text)` | 10.1 | Contiene "5" |
| `grade_10_2(text)` | 10.2 | Contiene "0.05" o "5 cents" |
| `grade_10_3(text)` | 10.3 | Identifica >= 2 de 3 bugs |
| `grade_11_1(text)` | 11.1 | Tiene tag de categoria Y estructura de ticket |
| `grade_11_2_math(text)` | 11.2a | NO responde "12" |
| `grade_11_2_off(text)` | 11.2b | Redirige con "focus"/"instead"/etc |
| `grade_11_3(text)` | 11.3 | JSON valido con keys: answer, confidence, sources_needed |

**Constantes compartidas:** `EMAILS_6` (4 emails de prueba), `ANSWERS_6`, `REGEX_6_1`, `REGEX_6_2`

### utils/data.py - Documentos de referencia
- `MATTERPORT_DOC` (32,428 chars) - SEC filing 10-K 2023, usado en ejercicio 8.2
- `TAX_CODE` (16,628 chars) - Section 83 IRC, usado en ejercicio 9.1

---

## Ejercicios por tipo

### Ejercicios estandar (render_exercise)
Cap 1-5, 8: Solo PROMPT y opcionalmente SYSTEM_PROMPT/PREFILL

### Ejercicios multi-test (render_multi_test_exercise)
Cap 6 (6.1, 6.2) y Cap 7 (7.1): Loop sobre 4 emails, template con `{email}`

### Ejercicios con extended thinking (custom UI)
Cap 10 (10.1, 10.2, 10.3): Usan `get_completion_with_thinking()`, slider de budget_tokens, expander para pensamiento

### Ejercicios con dual-test (custom UI)
Cap 11 (11.2): Un system prompt, dos tests (matematica + off-topic), ambos deben pasar

### Ejercicios abiertos (custom UI, sin calificacion automatica)
Cap 9 (9.1, 9.2): Prompt builder con multiples campos, marcados como completados al ejecutar

### Demos interactivos (sin calificacion)
Cap 12.1, 12.2, 12.3: Demos de encadenamiento, tool use y RAG

---

## Convenciones Tecnicas

### Idioma
- **Markdown/explicaciones en paginas:** Espanol
- **Prompts de ejemplo:** Ingles (mejores resultados con Claude)
- **Codigo/variables:** Ingles
- **UI labels:** Espanol ("Ejecutar", "Ver pista", "Correcto", etc.)

### Modelo
- **Modelo:** `claude-opus-4-6` (Claude Opus 4.6)
- **Notebooks:** MODEL_NAME definido en notebook 00, compartido via `%store`
- **Web app:** MODEL_NAME hardcoded en `utils/api.py` linea 4

### Patron para agregar un nuevo ejercicio a la web app
1. Agregar funcion de calificacion en `utils/grading.py`
2. En la pagina correspondiente, importar la funcion y llamar `render_exercise()`
3. Si el ejercicio es multi-test, usar `render_multi_test_exercise()`
4. Si necesita extended thinking, crear UI custom con `get_completion_with_thinking()`
5. Actualizar el total de ejercicios en `utils/components.py` linea 32 (`total = 26`)

### Patron para agregar un nuevo capitulo a la web app
1. Crear `streamlit_app/pages/NN_Nombre.py` (Streamlit los ordena alfabeticamente)
2. Seguir la estructura: `render_sidebar()` -> `st.title()` -> `render_lesson()` -> ejercicios
3. Agregar funciones de calificacion en `utils/grading.py`
4. Actualizar `total` en `utils/components.py` y la tabla en `app.py`

### Patron para cambiar el modelo
1. Web app: editar `MODEL_NAME` en `streamlit_app/utils/api.py` linea 4
2. Notebooks: editar celda de setup en `00_Tutorial_Como_Empezar.ipynb`

---

## Deployment

### Streamlit Cloud
- **URL:** https://prompt-eng-interactive-tutorial-2uvqtvg3te5ugk5phb35kq.streamlit.app
- **Config:** Repo `Ag1l1ty/prompt-eng-interactive-tutorial`, branch `master`, main file `streamlit_app/app.py`
- **Auto-deploy:** Push a `master` trigger redeploy automatico
- **Secrets:** Ninguno - usuarios ingresan su propia API key

### Local
```bash
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

---

## Tareas Completadas

1. **Fork y reestructurar** - Archivos movidos de `Anthropic 1P/` a raiz con nombres en espanol. `AmazonBedrock/` eliminado.
2. **Capitulo 10: Pensamiento Extendido** - Extended thinking API, budget_tokens, comparaciones, 3 ejercicios.
3. **Capitulo 11: System Prompts Avanzados** - Multi-seccion XML, personas, guardrails, formato JSON, 3 ejercicios.
4. **README.md en espanol** - Tabla de contenidos, instrucciones de instalacion, estructura del curso.
5. **Modelos actualizados a Claude Opus 4.6** - Todos los notebooks usan `MODEL_NAME = "claude-opus-4-6"`.
6. **Bugs corregidos** - #56, #61, #48, #11, #10, #43, #2.
7. **Traduccion completa** - 15 notebooks con markdown en espanol, prompts en ingles.
8. **Tool Use modernizado (12.2)** - Reescrito con API nativa: `tools`, JSON Schema, `ToolUseBlock`, bucle agentico.
9. **Streamlit Web App** - 14 paginas, 26 ejercicios, extended thinking, tool use, deployed en Streamlit Cloud.

## Bugs del Repo Original (referencia)

| Issue | Titulo | Estado |
|-------|--------|--------|
| #56 | hints module not found | CORREGIDO |
| #61 | Tool Use appendix usa modelo deprecado | CORREGIDO |
| #48 | Cap 8 conflates hallucination techniques | CORREGIDO |
| #11 | Typo "handilgj" en Tool Use appendix | CORREGIDO |
| #10 | f-string missing en Cap 9 | CORREGIDO |
| #43 | Link 404 system prompts | CORREGIDO |
| #2 | Add LICENSE file | CORREGIDO |
| #21 | Insecure API key usage | MITIGADO |
