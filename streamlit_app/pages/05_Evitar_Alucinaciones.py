import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.api import get_completion
from utils.grading import grade_5_1, grade_5_2
from utils.data import MATTERPORT_DOC

render_sidebar()
st.title("Capitulo 5: Evitar Alucinaciones")

render_lesson("""
### Que son las alucinaciones?

Las **alucinaciones** ocurren cuando Claude genera informacion que suena convincente
pero es **falsa o inventada**. Esto puede pasar cuando:

- Se le pregunta sobre hechos que no conoce
- La pregunta asume una premisa incorrecta
- Se le pide informacion muy especifica sin contexto suficiente

Las alucinaciones son uno de los mayores riesgos al trabajar con LLMs. Afortunadamente,
hay tecnicas efectivas para reducirlas drasticamente.

---

### Tecnica 1: Darle una salida a Claude

La tecnica mas simple y poderosa es **decirle explicitamente a Claude que admita
cuando no sabe algo**. Frases como:

- "Si no tienes informacion confiable, di que no lo sabes."
- "Si no estas seguro, indica tu nivel de incertidumbre."
- "Si la premisa de la pregunta es incorrecta, senalalo."

Esto reduce drasticamente las alucinaciones porque le das a Claude **permiso para
ser honesto** sobre sus limitaciones.

> **Sin proteccion:** "Quien gano el Premio Nobel de Fisica en 2030?"
>
> *Claude inventa una respuesta con nombre, universidad y contribucion -- todo falso.*

> **Con proteccion:** "Quien gano el Premio Nobel de Fisica en 2030? Si no tienes informacion confiable, di que no lo sabes."
>
> *Claude admite que no tiene esa informacion y explica por que.*

---

### Tecnica 2: Citar antes de responder

Para preguntas basadas en un **documento de referencia**, puedes pedirle a Claude que
**primero extraiga citas relevantes** del texto y luego responda basandose unicamente
en esas citas. Esto fuerza a Claude a anclar su respuesta en evidencia real.

La estructura recomendada es:

1. Incluir el documento en tags XML (ej: `<documento>...</documento>`)
2. Pedir a Claude que extraiga citas relevantes en tags `<citas>`
3. Instruirle que responda **SOLO** si las citas soportan la respuesta
4. Si las citas no son suficientes, que lo indique claramente

> **Sin citas:** "Segun el documento, cual es el ingreso anual?"
>
> *Claude podria inventar un numero si no lo encuentra claramente.*

> **Con citas primero:** "Primero extrae las citas relevantes del documento en tags
> `<citas>`. Luego responde basandote SOLO en las citas extraidas. Si no hay
> citas suficientes, di que la informacion no esta disponible en el documento."
>
> *Claude busca evidencia antes de responder, reduciendo errores.*

---

### Metacognicion: pedir autoevaluacion

Una tecnica avanzada es pedir a Claude que **evalue si tiene suficiente informacion**
antes de responder. Esto activa una forma de "metacognicion" donde Claude:

1. Analiza lo que sabe y lo que no
2. Evalua la calidad de su conocimiento
3. Decide si puede responder con confianza

> "Antes de responder, evalua si tienes informacion suficiente y confiable
> para dar una respuesta precisa. Si no la tienes, explica que te falta."

---

### Resumen de tecnicas

| Tecnica | Cuando usarla |
|---------|---------------|
| Darle una salida | Preguntas de conocimiento general |
| Citar antes de responder | Preguntas sobre documentos especificos |
| Metacognicion | Preguntas complejas o ambiguas |
""")

st.divider()
st.header("Ejercicios")

# ── Ejercicio 5.1 ──────────────────────────────────────────────
render_exercise(
    exercise_id="5.1",
    title="Evitar Alucinacion",
    instruction='''Claude tiene una tendencia a responder preguntas que asumen hechos falsos sin cuestionarlos.

Modifica este prompt para que Claude **admita que no puede confirmar** la premisa en vez de alucinar una respuesta:

> "En que fecha se lanzo el octavo album de estudio de Beyonce?"

*Nota: Beyonce tiene 7 albumes de estudio, no 8. Claude debe reconocer que la premisa es incorrecta.*''',
    hint="Agrega una instruccion como 'Si la premisa de la pregunta es incorrecta o no tienes informacion confiable, dilo claramente.'",
    grade_fn=grade_5_1,
)

# ── Documento de referencia para ejercicio 5.2 ─────────────────
st.subheader("Ejercicio 5.2 - Citar Antes de Responder")

with st.expander("Ver documento de referencia (Matterport 10-K)"):
    st.text(MATTERPORT_DOC[:3000] + "\n\n... [documento completo disponible para copiar] ...")
    st.code(MATTERPORT_DOC, language=None)

render_exercise(
    exercise_id="5.2",
    title="Citar Antes de Responder",
    instruction='''Tienes acceso a un documento largo (un informe financiero de Matterport). Tu tarea es escribir un prompt que:

1. Incluya el documento como contexto
2. Le pida a Claude que **primero extraiga citas relevantes** en tags `<citas>`
3. Luego responda la pregunta basandose SOLO en las citas

**Pregunta:** "Cuanto crecio la base de suscriptores de Matterport?"

*La respuesta correcta menciona un crecimiento de "49-fold" (49 veces).*

Expande la seccion de arriba para ver el documento completo y copiarlo en tu prompt.''',
    hint="Estructura tu prompt: 1) Instruccion de extraer citas primero. 2) El documento en tags <documento>. 3) La pregunta. 4) Instruccion de responder SOLO si las citas lo soportan.",
    grade_fn=grade_5_2,
)
