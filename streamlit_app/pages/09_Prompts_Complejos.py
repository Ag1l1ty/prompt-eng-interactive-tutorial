import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion
from utils.data import TAX_CODE

render_sidebar()

st.title("Capitulo 9: Prompts Complejos desde Cero")

render_lesson("""
## Construyendo Prompts Complejos

Felicidades por llegar al ultimo capitulo! Ahora es momento de unir todo y aprender a **crear prompts unicos y complejos**.

A continuacion, utilizaras una **estructura guiada que recomendamos para prompts complejos**. Te mostraremos algunos prompts especificos de la industria y explicaremos como estan estructurados.

**Nota:** **No todos los prompts necesitan cada elemento de la siguiente estructura compleja**. Te animamos a experimentar e incluir o excluir elementos y ver como afecta la respuesta de Claude. Generalmente es **mejor usar muchos elementos de prompt para que tu prompt funcione primero, y luego refinar y reducir tu prompt despues**.

---

### Estructura Recomendada para Prompts Complejos

El siguiente es el orden recomendado de los elementos de un prompt complejo. **El orden importa para algunos elementos**, pero no para todos:

1. **Contexto de la tarea** -- Dale a Claude contexto sobre el rol que debe asumir o que objetivos y tareas generales quieres que realice.
2. **Contexto de tono** -- Si es importante, dile a Claude que tono debe usar.
3. **Descripcion detallada de la tarea y reglas** -- Expande las tareas especificas y cualquier regla que Claude deba seguir. Dale una "salida" si no tiene respuesta.
4. **Ejemplos** -- Proporciona al menos un ejemplo de una respuesta ideal. Encierra esto en etiquetas XML `<example></example>`. Generalmente mas ejemplos = mejor.
5. **Datos de entrada a procesar** -- Si hay datos que Claude necesita procesar, incluyelos dentro de etiquetas XML relevantes.
6. **Descripcion inmediata de la tarea** -- "Recuerdale" a Claude exactamente lo que se espera que haga. Es mejor hacer esto hacia el final de un prompt largo.
7. **Precognicion** -- Para tareas complejas, dile a Claude que piense paso a paso antes de responder.
8. **Formato de salida** -- Si hay un formato especifico que quieres, especificalo claramente.
9. **Pre-llenado (prefill)** -- Opcionalmente, comienza la respuesta de Claude con algunas palabras para guiar su comportamiento.

---

### Ejemplo: Chatbot de Orientacion Profesional

Para ilustrar, construyamos un prompt para un juego de roles controlado donde Claude asume el rol de un orientador profesional:

```python
# Contexto de la tarea
TASK_CONTEXT = "You will be acting as an AI career coach named Joe created by the company AdAstra Careers.
Your goal is to give career advice to users."

# Contexto de tono
TONE_CONTEXT = "You should maintain a friendly customer service tone."

# Reglas detalladas
TASK_DESCRIPTION = \"\"\"Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say "Sorry, I didn't understand that. Could you rephrase your question?"
- If someone asks something irrelevant, say "Sorry, I am Joe and I give career advice."\"\"\"

# Datos de entrada (historial de conversacion + pregunta)
INPUT_DATA = f"<conversation_history>{{HISTORY}}</conversation_history>"
IMMEDIATE_TASK = f"Please respond to the user's most recent question: {{QUESTION}}"

# Precognicion
PRECOGNITION = "Think about the user's question in <career_advice> tags before answering."

# Formato de salida
OUTPUT_FORMATTING = "Put your response in <response> tags."

# Pre-llenado
PREFILL = "<career_advice>"
```

Cada elemento contribuye a un prompt completo y bien estructurado que produce respuestas consistentes y de alta calidad.

---

### Ejemplo: Servicios Legales

Los prompts dentro de la profesion legal pueden ser bastante complejos debido a la necesidad de:
- Analizar documentos largos
- Tratar con temas complejos
- Formatear la salida de maneras muy especificas
- Seguir procesos analiticos de multiples pasos

En este caso, se puede **cambiar el orden de algunos elementos** para mostrar que la estructura del prompt puede ser flexible. **La ingenieria de prompts se trata de prueba y error cientifico**. Te animamos a mezclar y combinar, mover cosas, y ver que funciona mejor para ti y tus necesidades.

---

### Resumen de la estructura

| # | Elemento | Posicion sugerida | Obligatorio? |
|---|----------|-------------------|-------------|
| 1 | Contexto de la tarea | Principio | Si |
| 2 | Contexto de tono | Principio | No |
| 3 | Reglas detalladas | Principio/Medio | Si |
| 4 | Ejemplos | Medio | Recomendado |
| 5 | Datos de entrada | Medio | Segun la tarea |
| 6 | Tarea inmediata | Final | Si |
| 7 | Precognicion | Final | Recomendado |
| 8 | Formato de salida | Final | No |
| 9 | Pre-llenado | Rol assistant | No |
""")

st.divider()
st.header("Ejercicios")

st.markdown("""
Los siguientes ejercicios son **abiertos** -- no tienen calificacion automatica.
El objetivo es que practiques la construccion de prompts complejos usando la estructura que acabas de aprender.
Revisa la respuesta de Claude y ajusta tu prompt iterativamente hasta obtener un resultado satisfactorio.
""")

# ---------------------------------------------------------------------------
# Exercise 9.1 - Financial Services Chatbot
# ---------------------------------------------------------------------------
st.subheader("Ejercicio 9.1 - Chatbot de Servicios Financieros")
st.markdown("""
Los prompts dentro de la profesion financiera tambien pueden ser bastante complejos por razones similares a los prompts legales. En este ejercicio, construiras un prompt complejo para un **asistente de contabilidad fiscal** que responde preguntas usando un documento del codigo fiscal.

**Tu tarea:** Llena los campos de elementos del prompt para construir un prompt complejo. El prompt debe:
- Darle a Claude un rol de asesor fiscal
- Incluir reglas para manejar preguntas fuera de tema
- Referenciar el documento del codigo fiscal
- Pedir a Claude que piense paso a paso
- Especificar un formato de salida

**Pregunta del usuario:** `"How long do I have to make an 83b election?"`

**Documento del codigo fiscal** (disponible abajo para copiar):
""")

with st.expander("Ver documento del codigo fiscal (Section 83 - IRC)"):
    st.code(TAX_CODE, language=None)
    st.caption("Copia este texto y referencialo en tu prompt usando etiquetas XML como <tax_code>...</tax_code>.")

st.markdown("---")
st.markdown("**Construye tu prompt complejo rellenando los elementos que necesites:**")

task_context_91 = st.text_area(
    "Contexto de la tarea (rol y objetivo)",
    placeholder="Ej: You will be acting as an AI tax accountant assistant...",
    height=80,
    key="task_context_91",
)
tone_context_91 = st.text_area(
    "Contexto de tono (opcional)",
    placeholder="Ej: You should maintain a professional and helpful tone...",
    height=60,
    key="tone_context_91",
)
task_description_91 = st.text_area(
    "Descripcion detallada y reglas",
    placeholder="Ej: Here are the important rules for the interaction:\n- Always reference the tax code...\n- If the question is not related to taxes, say...",
    height=120,
    key="task_desc_91",
)
examples_91 = st.text_area(
    "Ejemplos (opcional)",
    placeholder="Ej: <example>User: What is the deadline...\\nAssistant: According to...</example>",
    height=100,
    key="examples_91",
)
input_data_91 = st.text_area(
    "Datos de entrada (documento fiscal + pregunta)",
    placeholder="Ej: <tax_code>...</tax_code>\n<question>How long do I have to make an 83b election?</question>",
    height=150,
    key="input_data_91",
)
immediate_task_91 = st.text_area(
    "Tarea inmediata",
    placeholder="Ej: Please respond to the user's question using the provided tax code...",
    height=80,
    key="immediate_task_91",
)
precognition_91 = st.text_area(
    "Precognicion (opcional)",
    placeholder="Ej: Before answering, think step by step in <thinking> tags...",
    height=60,
    key="precog_91",
)
output_format_91 = st.text_area(
    "Formato de salida (opcional)",
    placeholder="Ej: Put your final answer in <answer> tags.",
    height=60,
    key="output_91",
)
prefill_91 = st.text_input(
    "Pre-llenado (opcional)",
    placeholder="Ej: <thinking>",
    key="prefill_91",
)

# Combine elements
prompt_parts_91 = [
    task_context_91,
    tone_context_91,
    task_description_91,
    examples_91,
    input_data_91,
    immediate_task_91,
    precognition_91,
    output_format_91,
]
combined_prompt_91 = "\n\n".join(p for p in prompt_parts_91 if p.strip())

col_preview_91, col_run_91 = st.columns([1, 1])
with col_preview_91:
    if st.button("Ver prompt completo", key="preview_91"):
        st.markdown("**Prompt combinado:**")
        st.code(combined_prompt_91 if combined_prompt_91.strip() else "(vacio)", language=None)
        if prefill_91:
            st.markdown("**Pre-llenado (assistant):**")
            st.code(prefill_91, language=None)

with col_run_91:
    if st.button("Ejecutar", key="run_91"):
        if not combined_prompt_91.strip():
            st.warning("Escribe al menos un elemento del prompt antes de ejecutar.")
        else:
            with st.spinner("Claude esta pensando..."):
                response = get_completion(combined_prompt_91, prefill=prefill_91)
            st.markdown("**Respuesta de Claude:**")
            st.code(response, language=None)
            st.success("Revisa la respuesta de Claude. No hay calificacion automatica para este ejercicio.")
            st.session_state.completed.add("9.1")

with st.expander("Ver pista / posible solucion"):
    st.markdown("""
**Pista:** Una buena solucion incluye:
- **Contexto:** "You will be acting as an AI tax accountant assistant..."
- **Reglas:** Decirle a Claude que solo responda sobre temas fiscales, que cite el codigo fiscal
- **Datos:** Incluir el codigo fiscal en etiquetas `<tax_code>` y la pregunta en `<question>`
- **Tarea inmediata:** "Answer the user's question using the provided tax code"
- **Precognicion:** "Think step by step about the relevant sections before answering"
- **Formato:** "Put your answer in `<answer>` tags"

La respuesta correcta a la pregunta es que la eleccion 83(b) debe hacerse **dentro de los 30 dias** posteriores a la transferencia de propiedad.
""")

st.divider()

# ---------------------------------------------------------------------------
# Exercise 9.2 - Codebot
# ---------------------------------------------------------------------------
st.subheader("Ejercicio 9.2 - Codebot (Tutor Socratico de Codigo)")
st.markdown("""
En este ejercicio, escribiras un prompt para un **bot de asistencia y ensenanza de codigo que lee codigo y ofrece correcciones guiadas cuando sea apropiado**.

El bot deberia actuar como un **tutor socratico**: en lugar de simplemente dar la respuesta, deberia guiar al estudiante a descubrir el error por si mismo.

**Codigo del usuario:**
```python
# Funcion para imprimir inversos multiplicativos
def print_multiplicative_inverses(x, n):
  for i in range(n):
    print(x / i)
```

**Nota:** Este codigo tiene un bug -- cuando `i = 0`, se produce un error de division por cero.

**Tu tarea:** Construye un prompt complejo que haga que Claude:
- Actue como un tutor de programacion amigable
- Use el metodo socratico (preguntas guiadas en lugar de dar la respuesta directamente)
- Lea el codigo proporcionado e identifique problemas
- Guie al estudiante hacia la solucion
""")

st.markdown("---")
st.markdown("**Construye tu prompt complejo rellenando los elementos que necesites:**")

CODE_92 = """
# Funcion para imprimir inversos multiplicativos
def print_multiplicative_inverses(x, n):
  for i in range(n):
    print(x / i)
"""

task_context_92 = st.text_area(
    "Contexto de la tarea (rol y objetivo)",
    placeholder="Ej: You are a Socratic coding tutor who helps students learn by guiding them with questions...",
    height=80,
    key="task_context_92",
)
tone_context_92 = st.text_area(
    "Contexto de tono (opcional)",
    placeholder="Ej: Be encouraging, patient, and supportive...",
    height=60,
    key="tone_context_92",
)
task_description_92 = st.text_area(
    "Descripcion detallada y reglas",
    placeholder="Ej: Important rules:\n- Never give the answer directly\n- Ask guiding questions\n- Point out which line might have an issue...",
    height=120,
    key="task_desc_92",
)
examples_92 = st.text_area(
    "Ejemplos (opcional)",
    placeholder="Ej: <example>\nStudent code: ...\nYour response: What happens when the variable is 0?...\n</example>",
    height=100,
    key="examples_92",
)
input_data_92 = st.text_area(
    "Datos de entrada (codigo del usuario)",
    value=f"<code>{CODE_92}</code>",
    height=120,
    key="input_data_92",
)
immediate_task_92 = st.text_area(
    "Tarea inmediata",
    placeholder="Ej: Review the student's code above and provide Socratic guidance...",
    height=80,
    key="immediate_task_92",
)
precognition_92 = st.text_area(
    "Precognicion (opcional)",
    placeholder="Ej: First, analyze the code for bugs in <analysis> tags, then formulate guiding questions...",
    height=60,
    key="precog_92",
)
output_format_92 = st.text_area(
    "Formato de salida (opcional)",
    placeholder="Ej: Put your guiding questions in <guidance> tags.",
    height=60,
    key="output_92",
)
prefill_92 = st.text_input(
    "Pre-llenado (opcional)",
    placeholder="Ej: <analysis>",
    key="prefill_92",
)

# Combine elements
prompt_parts_92 = [
    task_context_92,
    tone_context_92,
    task_description_92,
    examples_92,
    input_data_92,
    immediate_task_92,
    precognition_92,
    output_format_92,
]
combined_prompt_92 = "\n\n".join(p for p in prompt_parts_92 if p.strip())

col_preview_92, col_run_92 = st.columns([1, 1])
with col_preview_92:
    if st.button("Ver prompt completo", key="preview_92"):
        st.markdown("**Prompt combinado:**")
        st.code(combined_prompt_92 if combined_prompt_92.strip() else "(vacio)", language=None)
        if prefill_92:
            st.markdown("**Pre-llenado (assistant):**")
            st.code(prefill_92, language=None)

with col_run_92:
    if st.button("Ejecutar", key="run_92"):
        if not combined_prompt_92.strip():
            st.warning("Escribe al menos un elemento del prompt antes de ejecutar.")
        else:
            with st.spinner("Claude esta pensando..."):
                response = get_completion(combined_prompt_92, prefill=prefill_92)
            st.markdown("**Respuesta de Claude:**")
            st.code(response, language=None)
            st.success("Revisa la respuesta de Claude. No hay calificacion automatica para este ejercicio.")
            st.session_state.completed.add("9.2")

with st.expander("Ver pista / posible solucion"):
    st.markdown("""
**Pista:** Una buena solucion incluye:
- **Contexto:** "You are a Socratic coding tutor. Your goal is to help students learn to debug code by guiding them with questions rather than giving direct answers."
- **Tono:** "Be encouraging, patient, and pedagogical."
- **Reglas:** "Never reveal the bug directly. Instead, ask questions that lead the student to discover the issue themselves. Point to specific lines and ask what might happen with certain inputs."
- **Datos:** El codigo en etiquetas `<code>`
- **Tarea:** "Review the student's code and help them find and fix any bugs using the Socratic method."
- **Precognicion:** "First analyze the code in `<analysis>` tags to identify all bugs, then formulate guiding questions."

El bug principal es la **division por cero** cuando `i = 0` en la primera iteracion del `range(n)`.
""")

st.divider()

# ---------------------------------------------------------------------------
# Congratulations
# ---------------------------------------------------------------------------
st.markdown("""
## Felicidades!

Si completaste todos los ejercicios, **ahora estas en el 0.1% superior de los ingenieros de prompts**. Uno de la elite!

Las tecnicas que has aprendido, desde pensar paso a paso hasta asignar roles, usar ejemplos y la escritura clara en general, pueden ser **combinadas, remezcladas y adaptadas de innumerables maneras**.

La ingenieria de prompts es una disciplina muy nueva, asi que manten una mente abierta. Tu podrias ser quien descubra el proximo gran truco de prompting.

### Proximos pasos:
- Aprende de ejemplos de prompts listos para produccion en el [cookbook de Anthropic](https://anthropic.com/cookbook)
- Lee la [guia de prompting](https://docs.anthropic.com/claude/docs/prompt-engineering)
- Consulta la [biblioteca de prompts](https://anthropic.com/prompts) para inspiracion
- Prueba el [metaprompt](https://docs.anthropic.com/claude/docs/helper-metaprompt-experimental) experimental
- Haz preguntas en el [servidor de Discord](https://anthropic.com/discord) de Anthropic
""")
