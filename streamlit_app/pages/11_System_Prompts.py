import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.api import get_completion
from utils.grading import grade_11_1, grade_11_2_math, grade_11_2_off, grade_11_3

render_sidebar()

st.title("Capitulo 11: System Prompts Avanzados")

render_lesson("""
## Tecnicas Avanzadas para System Prompts

En el **Capitulo 1**, introdujimos los system prompts como una forma de dar contexto e instrucciones a Claude.
En este capitulo, exploraremos tecnicas avanzadas para construir system prompts poderosos y bien estructurados.

### 1. System Prompts Multi-Seccion con Estructura XML

Los system prompts simples funcionan bien para tareas basicas, pero para comportamientos complejos, es mejor organizar
el system prompt en **secciones claramente definidas** usando tags XML.

Esto ayuda a Claude a entender las diferentes dimensiones de su comportamiento esperado:

```python
SYSTEM_PROMPT = \"\"\"<role>
You are a senior financial analyst at a Fortune 500 company.
You have 20 years of experience in corporate finance and M&A.
</role>

<instructions>
- Always provide data-driven analysis
- Cite specific metrics when available
- Consider both risks and opportunities
</instructions>

<output_format>
Structure every response as:
1. Executive Summary (2-3 sentences)
2. Detailed Analysis
3. Key Risks
4. Recommendations
</output_format>

<constraints>
- Never provide specific investment advice
- Always note that analysis is for informational purposes only
</constraints>\"\"\"
```

Las secciones XML actuan como **compartimentos mentales** que Claude puede consultar durante la generacion de su respuesta.

### 2. Definicion Detallada de Persona

Mas alla de un simple "You are a...", puedes definir personas con **multiples dimensiones**:
experiencia, estilo de comunicacion, valores, y hasta limitaciones:

```python
SYSTEM_PROMPT = \"\"\"<persona>
<name>Dr. Sarah Chen</name>
<background>PhD in Computer Science from MIT. 15 years in AI safety research.</background>
<communication_style>
- Uses analogies from everyday life to explain complex concepts
- Asks Socratic questions to guide understanding
- Acknowledges uncertainty openly
</communication_style>
<values>
- Intellectual honesty over reassurance
- Nuanced thinking over simplistic answers
</values>
</persona>\"\"\"
```

### 3. Guardrails de Comportamiento

Los guardrails son **reglas que definen lo que Claude debe y no debe hacer**. Son especialmente importantes
para aplicaciones de produccion:

```python
SYSTEM_PROMPT = \"\"\"<role>You are a children's educational assistant for ages 6-12.</role>

<allowed_topics>
- Science, math, history, geography, language arts
- Creative writing and storytelling
</allowed_topics>

<forbidden_topics>
- Violence, weapons, or warfare details
- Adult content of any kind
- Political opinions or partisan content
</forbidden_topics>

<behavioral_rules>
- If asked about a forbidden topic, say:
  "That's a great question to discuss with your parents or teacher!
   Let's talk about [redirect to related allowed topic]."
- Always encourage curiosity and asking questions
</behavioral_rules>\"\"\"
```

### 4. Formato de Output via System Prompts

Puedes usar system prompts para forzar formatos de output especificos, como JSON:

```python
SYSTEM_PROMPT = \"\"\"You are a data extraction API. You MUST respond ONLY with valid JSON, no other text.

For any user input, extract the following fields:
{
  "entities": [{"name": string, "type": "person|organization|location"}],
  "sentiment": "positive|negative|neutral",
  "topics": [string]
}

Rules:
- Always return valid JSON
- If a field cannot be determined, use null
- Never include explanations outside the JSON\"\"\"
```

### 5. System Prompt vs User Prompt: Cuando usar cada uno

| Aspecto | System Prompt | User Prompt |
|---------|--------------|-------------|
| Proposito | Comportamiento persistente | Tarea especifica |
| Alcance | Toda la conversacion | Un turno |
| Ejemplo | "Eres un experto en X" | "Analiza este texto" |
| Prioridad | Establece el contexto base | Define la accion |

**Regla general**: Pon en el system prompt todo lo que quieres que se aplique **siempre**
(rol, formato, restricciones). Pon en el user prompt lo que es **especifico a cada interaccion**
(datos, preguntas, tareas concretas).

### 6. Consideraciones sobre la longitud

- System prompts **cortos** (<500 tokens): Bien para tareas simples
- System prompts **medianos** (500-2000 tokens): Ideal para la mayoria de aplicaciones
- System prompts **largos** (>2000 tokens): Puede diluir la atencion de Claude

**Consejo**: Pon las instrucciones mas importantes al **principio** y al **final** del system prompt
(efecto de primacia y recencia).
""")

st.divider()
st.header("Ejercicios")

# ── Exercise 11.1 ────────────────────────────────────────────────────────────

render_exercise(
    exercise_id="11.1",
    title="Bot de Atencion al Cliente",
    instruction="""Escribe un system prompt **multi-seccion** (usando tags XML) para un bot de atencion al cliente que:

1. **Categorice** las quejas automaticamente (ej: envio, producto defectuoso, facturacion)
2. Responda con **empatia**
3. Proporcione un **numero de ticket** o referencia
4. **Estructure** su respuesta con secciones claras

El prompt del usuario sera una queja de un cliente:

> *"I ordered a laptop 3 weeks ago and it still hasn't arrived. I've tried calling support twice but nobody answers. This is unacceptable!"*

La calificacion busca que la respuesta contenga una **categoria** (como shipping/delivery) Y una **estructura con ticket/referencia**.""",
    hint="La funcion de calificacion busca una respuesta que contenga tags XML de estructura (<categoria>, <respuesta>, o similares).\nUsa multiples secciones en tu system prompt: <rol>, <instrucciones>, <formato>, <restricciones>.",
    grade_fn=grade_11_1,
    fields=[
        {"name": "SYSTEM_PROMPT", "label": "System Prompt", "rows": 8},
        {"name": "PROMPT", "label": "Prompt (mensaje del cliente)", "rows": 3},
    ],
    system_prompt_default="",
)

# ── Exercise 11.2 ────────────────────────────────────────────────────────────

st.subheader("Ejercicio 11.2 - Guardrails Educativos")
st.markdown("""Crea un system prompt para un **asistente de matematicas para ninos** que:

1. **Solo** responda preguntas de matematicas
2. **Rechace educadamente** temas no relacionados, redirigiendo al tema
3. Use un tono **amigable y motivador**
4. **Nunca de la respuesta directa**, solo guie al estudiante

Este ejercicio tiene **dos pruebas** que deben pasar con el **mismo system prompt**:

- **Test 1 - Pregunta matematica**: "What is 15% of 80?" -- Claude **NO** debe dar la respuesta directa (12),
  sino guiar al estudiante para que la descubra por si mismo.
- **Test 2 - Tema no relacionado**: "Tell me about dinosaurs" -- Claude debe **redirigir** amablemente
  hacia matematicas.

Ambas pruebas deben pasar para completar el ejercicio.""")

system_11_2 = st.text_area(
    "System Prompt",
    value="",
    height=250,
    key="ex_11_2_system",
)

col_hint_11_2, col_show_11_2 = st.columns([1, 4])
show_hint_11_2 = col_show_11_2.button("Ver pista", key="hint_11_2", use_container_width=True)
if show_hint_11_2:
    st.info("La funcion de calificacion busca que Claude rechace temas inapropiados y se mantenga en el tema educativo.\nIncluye restricciones claras en tu system prompt sobre que temas son permitidos y cuales no.")

# Track which sub-tests pass
key_math = "11.2_math_passed"
key_off = "11.2_off_passed"
if key_math not in st.session_state:
    st.session_state[key_math] = False
if key_off not in st.session_state:
    st.session_state[key_off] = False

col1, col2 = st.columns(2)

with col1:
    if st.button("Test: Pregunta matematica", key="run_11_2_math"):
        if not system_11_2.strip():
            st.warning("Escribe un system prompt antes de ejecutar.")
        else:
            with st.spinner("Claude pensando..."):
                response_math = get_completion(
                    "What is 15% of 80?", system_prompt=system_11_2
                )
            st.markdown("**Respuesta:**")
            st.code(response_math, language=None)

            if grade_11_2_math(response_math):
                st.success("Correcto! Claude no dio la respuesta directa (12).")
                st.session_state[key_math] = True
            else:
                st.error("Claude no deberia dar la respuesta directa '12'. Debe guiar al estudiante.")
                st.session_state[key_math] = False

with col2:
    if st.button("Test: Tema no relacionado", key="run_11_2_off"):
        if not system_11_2.strip():
            st.warning("Escribe un system prompt antes de ejecutar.")
        else:
            with st.spinner("Claude pensando..."):
                response_off = get_completion(
                    "Tell me about dinosaurs", system_prompt=system_11_2
                )
            st.markdown("**Respuesta:**")
            st.code(response_off, language=None)

            if grade_11_2_off(response_off):
                st.success("Correcto! Claude redirigio hacia matematicas.")
                st.session_state[key_off] = True
            else:
                st.error("Claude deberia redirigir temas no relacionados hacia matematicas.")
                st.session_state[key_off] = False

# Check overall completion
if st.session_state.get(key_math) and st.session_state.get(key_off):
    st.success("Ambas pruebas pasaron! Ejercicio 11.2 completado.")
    st.session_state.completed.add("11.2")
elif st.session_state.get(key_math) or st.session_state.get(key_off):
    passed_label = "matematica" if st.session_state.get(key_math) else "tema no relacionado"
    pending_label = "tema no relacionado" if st.session_state.get(key_math) else "matematica"
    st.warning(f"Prueba de {passed_label} pasada. Falta la prueba de {pending_label}.")

st.divider()

# ── Exercise 11.3 ────────────────────────────────────────────────────────────

render_exercise(
    exercise_id="11.3",
    title="Formato JSON Forzado",
    instruction="""Crea un system prompt que fuerce a Claude a **siempre** responder en formato JSON con esta estructura exacta:

```json
{
  "answer": "...",
  "confidence": "high|medium|low",
  "sources_needed": true|false
}
```

Prueba tu system prompt con cualquier pregunta, por ejemplo:
- "What is the capital of France?"
- "What will the stock market do tomorrow?"
- "Write me a poem about cats"

La calificacion verifica que la respuesta sea **JSON valido** y que contenga las tres claves: `answer`, `confidence`, y `sources_needed`.

**Consejo**: Puedes usar el prefill `{` para ayudar a Claude a empezar con JSON, pero un buen system prompt deberia ser suficiente.""",
    hint="La funcion de calificacion busca una respuesta en formato JSON valido.\nEn tu system prompt, incluye un esquema JSON de ejemplo y una instruccion explicita de que SIEMPRE responda en JSON, sin importar la pregunta.",
    grade_fn=grade_11_3,
    fields=[
        {"name": "SYSTEM_PROMPT", "label": "System Prompt", "rows": 8},
        {"name": "PROMPT", "label": "Prompt", "rows": 3},
    ],
    system_prompt_default="",
)

st.markdown("---")
st.markdown("Has completado los capitulos principales del tutorial! Continua a los **Apendices** para aprender sobre encadenamiento de prompts, uso de herramientas y busqueda/recuperacion.")
