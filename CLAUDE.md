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
├── 01-11, 12.1-12.3 *.ipynb               # 15 notebooks originales (legacy)
│
└── streamlit_app/                          # Web app interactiva (10 capitulos)
    ├── app.py                              # Pagina de inicio + API key + progreso
    ├── requirements.txt                    # streamlit>=1.29.0, anthropic>=0.39.0
    ├── .streamlit/config.toml              # Tema naranja personalizado
    ├── pages/                              # 10 capitulos (Streamlit multi-page)
    │   ├── 01_Ser_Claro_y_Directo.py       # Cap 1: 3 ejercicios (1.1-1.3)
    │   ├── 02_XML_Tags.py                  # Cap 2: 3 ejercicios (2.1-2.3)
    │   ├── 03_Formato_y_Prefill.py         # Cap 3: 3 ejercicios (3.1-3.3)
    │   ├── 04_Ejemplos_Few_Shot.py         # Cap 4: 3 multi-test (4.1-4.3)
    │   ├── 05_Evitar_Alucinaciones.py      # Cap 5: 2 ejercicios (5.1-5.2)
    │   ├── 06_Prompts_Complejos.py         # Cap 6: 2 abiertos (6.1-6.2)
    │   ├── 07_Pensamiento_Extendido.py     # Cap 7: 3 con thinking (7.1-7.3)
    │   ├── 08_System_Prompts.py            # Cap 8: 3 ejercicios (8.1-8.3)
    │   ├── 09_Herramientas.py              # Cap 9: 3 demos interactivos
    │   └── 10_RAG.py                       # Cap 10: 3 demos interactivos
    └── utils/
        ├── __init__.py
        ├── api.py                          # Claude API wrapper (3 funciones)
        ├── components.py                   # UI reutilizable (6 componentes)
        ├── grading.py                      # 24 funciones de calificacion
        └── data.py                         # Documentos de referencia (Cap 5, 6)
```

---

## Estructura del Curso (10 Capitulos)

### Fundamentos
| Cap | Pagina | Tema | Ejercicios |
|-----|--------|------|------------|
| 1 | `01_Ser_Claro_y_Directo.py` | Ser Claro y Directo | 1.1, 1.2, 1.3 |
| 2 | `02_XML_Tags.py` | Estructurar con XML Tags | 2.1, 2.2, 2.3 |
| 3 | `03_Formato_y_Prefill.py` | Formato de Output y Prefill | 3.1, 3.2, 3.3 |
| 4 | `04_Ejemplos_Few_Shot.py` | Ejemplos y Few-Shot | 4.1, 4.2, 4.3 |
| 5 | `05_Evitar_Alucinaciones.py` | Evitar Alucinaciones | 5.1, 5.2 |

### Avanzado
| Cap | Pagina | Tema | Ejercicios |
|-----|--------|------|------------|
| 6 | `06_Prompts_Complejos.py` | Prompts Complejos desde Cero | 6.1, 6.2 |
| 7 | `07_Pensamiento_Extendido.py` | Pensamiento Extendido | 7.1, 7.2, 7.3 |
| 8 | `08_System_Prompts.py` | System Prompts Avanzados | 8.1, 8.2, 8.3 |
| 9 | `09_Herramientas.py` | Herramientas y Agentes | demos |
| 10 | `10_RAG.py` | RAG: Busqueda y Recuperacion | demos |

**Total de ejercicios calificados: 24** (configurado en `components.py` linea 32)

### Capitulos eliminados/absorbidos vs tutorial original de 14
- Cap 1 original (Estructura Basica) - Eliminado: era solo API basics
- Cap 3 original (Roles) - Absorbido en Cap 8 (System Prompts)
- Cap 6 original (Precognicion/CoT) - Absorbido en Cap 7 (Extended Thinking lo reemplaza)
- Cap 12.1 (Encadenamiento) - Absorbido como bonus en Cap 6 (Prompts Complejos)

---

## Arquitectura de la Web App (Streamlit)

### Punto de entrada
- `streamlit_app/app.py` - Home page con API key input en sidebar y tabla de contenidos
- Streamlit descubre automaticamente las paginas en `pages/` y las muestra en el menu lateral

### Session State
```python
st.session_state.api_key    # str - API key de Anthropic
st.session_state.completed  # set - IDs de ejercicios completados (ej: {"1.1", "2.3", "7.1"})
```

### utils/api.py - Funciones de la API de Claude
| Funcion | Uso | Parametros clave |
|---------|-----|------------------|
| `get_client()` | Crea client Anthropic desde session_state | - |
| `get_completion(prompt, system_prompt, prefill)` | Llamada estandar | temp=0.0, max_tokens=2000 |
| `get_completion_with_thinking(prompt, system_prompt, budget_tokens)` | Extended thinking (Cap 7) | max_tokens=16000, retorna (thinking, response) |
| `run_tool_loop(user_message, tools, available_functions, system_prompt)` | Bucle agentico (Cap 9) | max 5 iteraciones, retorna (text, tool_log) |

**Modelo:** `claude-opus-4-6` (hardcoded en `MODEL_NAME` variable, linea 4)

### utils/components.py - Componentes UI reutilizables
| Componente | Descripcion |
|------------|-------------|
| `init_session()` | Inicializa session_state (api_key, completed) |
| `render_sidebar()` | Sidebar con API key, barra de progreso (24 total), link a GitHub |
| `render_lesson(content)` | Renderiza markdown de leccion |
| `render_exercise(exercise_id, title, instruction, hint, grade_fn, fields, prefill, system_prompt_default)` | Ejercicio completo con inputs, ejecucion, calificacion |
| `render_multi_test_exercise(exercise_id, title, instruction, hint, test_cases, grade_fn, prompt_template, prefill)` | Ejercicio con multiples casos de prueba (Cap 4) |
| `render_code_demo(prompt, system_prompt, label)` | Demo ejecutable en expander |

### utils/grading.py - Funciones de calificacion

#### Cap 1 - Ser Claro y Directo
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_1_1(text)` | 1.1 | Exactamente "Michael Jordan" |
| `grade_1_2(text)` | 1.2 | Contiene "incorrecto"/"incorrect" (bilingue) |
| `grade_1_3(text)` | 1.3 | >= 800 palabras |

#### Cap 2 - XML Tags
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_2_1(text)` | 2.1 | Contiene "cerdo"/"pig" Y "haiku" |
| `grade_2_2(text)` | 2.2 | Contiene "brown"/"marron"/"cafe" (bilingue) |
| `grade_2_3(text)` | 2.3 | Igual que 2.2 (minimo contexto) |

#### Cap 3 - Formato y Prefill
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_3_1(text)` | 3.1 | Contiene "Warrior"/"Warriors"/"Golden State" |
| `grade_3_2(text)` | 3.2 | Contiene "cat"/"gato", `<haiku>`, >5 lineas |
| `grade_3_3(text)` | 3.3 | Contiene "tail"/"cola", "cat"/"gato", `<haiku>` |

#### Cap 4 - Few-Shot (multi-test con EMAILS_4)
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_4_1(response, tc)` | 4.1 | Letra correcta con parentesis: `B)` |
| `grade_4_2(response, tc)` | 4.2 | Letra en tags XML: `<answer>B</answer>` |
| `grade_4_3(response, tc)` | 4.3 | Ultimo caracter = letra correcta |

**Constantes:** `EMAILS_4` (4 emails en espanol), `ANSWERS_4`, `REGEX_4_1`, `REGEX_4_2`

#### Cap 5 - Evitar Alucinaciones
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_5_1(text)` | 5.1 | Admite no saber ("no se"/"unfortunately") Y NO contiene "2022" |
| `grade_5_2(text)` | 5.2 | Contiene "49-fold"/"49 veces"/"49x" |

#### Cap 6 - Prompts Complejos
Ejercicios 6.1 y 6.2 son abiertos - se marcan completados al ejecutar.

#### Cap 7 - Pensamiento Extendido
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_7_1(text)` | 7.1 | Contiene "5" (problema de maquinas) |
| `grade_7_2(text)` | 7.2 | Contiene "0.05"/"5 cents"/"5 centavos" (bat-and-ball) |
| `grade_7_3(text)` | 7.3 | Identifica >= 2 de 3 bugs en code review |

#### Cap 8 - System Prompts
| Funcion | Ejercicio | Verifica |
|---------|-----------|----------|
| `grade_8_1(text)` | 8.1 | Tiene tag de categoria Y estructura de ticket |
| `grade_8_2_math(text)` | 8.2a | NO responde "12" directamente |
| `grade_8_2_off(text)` | 8.2b | Redirige con "math"/"focus"/"matematica"/etc |
| `grade_8_3(text)` | 8.3 | JSON valido con keys: answer, confidence, sources_needed |

### utils/data.py - Documentos de referencia
- `MATTERPORT_DOC` (32,428 chars) - SEC filing 10-K 2023, usado en ejercicio 5.2
- `TAX_CODE` (16,628 chars) - Section 83 IRC, usado en ejercicio 6.1

---

## Ejercicios por tipo

### Ejercicios estandar (render_exercise)
Cap 1 (1.1-1.3), Cap 2 (2.1-2.3), Cap 3 (3.1-3.3), Cap 5 (5.1-5.2), Cap 8 (8.1, 8.3)
Solo PROMPT y opcionalmente SYSTEM_PROMPT/PREFILL.

### Ejercicios multi-test (render_multi_test_exercise)
Cap 4 (4.1, 4.2, 4.3): Loop sobre 4 emails (EMAILS_4), template con `{email}`

### Ejercicios con extended thinking (custom UI)
Cap 7 (7.1, 7.2, 7.3): Usan `get_completion_with_thinking()`, slider de budget_tokens, expander para pensamiento

### Ejercicios con dual-test (custom UI)
Cap 8 (8.2): Un system prompt, dos tests (matematica + off-topic), ambos deben pasar

### Ejercicios abiertos (custom UI, sin calificacion automatica)
Cap 6 (6.1, 6.2): Prompt builder con multiples campos, marcados como completados al ejecutar

### Demos interactivos (sin calificacion)
Cap 9 (Herramientas): Calculadora, cuando Claude no usa tools, mini base de datos
Cap 10 (RAG): RAG basico, multiples documentos, deteccion de limites

---

## Convenciones Tecnicas

### Idioma
- **Todo el contenido visible al usuario:** Espanol (lecciones, prompts de ejemplo, UI, instrucciones)
- **Codigo/variables:** Ingles
- **Grading:** Bilingue - regex aceptan respuestas en espanol O ingles

### Modelo
- **Modelo:** `claude-opus-4-6` (Claude Opus 4.6)
- **Notebooks:** MODEL_NAME definido en notebook 00, compartido via `%store`
- **Web app:** MODEL_NAME hardcoded en `utils/api.py` linea 4

### Patron para agregar un nuevo ejercicio a la web app
1. Agregar funcion de calificacion en `utils/grading.py`
2. En la pagina correspondiente, importar la funcion y llamar `render_exercise()`
3. Si el ejercicio es multi-test, usar `render_multi_test_exercise()`
4. Si necesita extended thinking, crear UI custom con `get_completion_with_thinking()`
5. Actualizar el total de ejercicios en `utils/components.py` linea 32 (`total = 24`)

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

1. **Fork y reestructurar** - Archivos movidos de `Anthropic 1P/` a raiz con nombres en espanol.
2. **Capitulo 10: Pensamiento Extendido** - Extended thinking API, budget_tokens, comparaciones, 3 ejercicios.
3. **Capitulo 11: System Prompts Avanzados** - Multi-seccion XML, personas, guardrails, formato JSON, 3 ejercicios.
4. **README.md en espanol** - Tabla de contenidos, instrucciones de instalacion, estructura del curso.
5. **Modelos actualizados a Claude Opus 4.6** - Todos los notebooks usan `claude-opus-4-6`.
6. **Bugs corregidos** - #56, #61, #48, #11, #10, #43, #2.
7. **Traduccion completa** - 15 notebooks con markdown en espanol.
8. **Tool Use modernizado (12.2)** - Reescrito con API nativa.
9. **Streamlit Web App v1** - 14 paginas, 26 ejercicios, deployed en Streamlit Cloud.
10. **Reestructuracion a 10 capitulos** - Eliminados capitulos redundantes (API basics, roles, CoT, encadenamiento). Prompts en espanol. Grading bilingue. 24 ejercicios. Sin patron print(get_completion()).

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
