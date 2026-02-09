import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.api import get_completion
from utils.grading import grade_8_1, grade_8_2_math, grade_8_2_off, grade_8_3

render_sidebar()
st.title("Capitulo 8: System Prompts Avanzados")

render_lesson("""
### System prompt vs. prompt de usuario

En la API de Claude hay dos niveles de instruccion:

- **System prompt:** Contexto global y persistente. Define *quien es* Claude y *como debe comportarse* en toda la conversacion.
- **Prompt de usuario:** Instruccion por turno. Define *que hacer* en este momento especifico.

Piensa en el system prompt como las **reglas del juego** y el prompt de usuario como
una **jugada especifica** dentro de esas reglas.

---

### Roles como fundamento

La forma mas basica y efectiva de usar un system prompt es **asignar un rol**.
Un rol bien definido ancla todo el comportamiento de Claude:

> **System prompt simple:** "Eres un abogado especializado en propiedad intelectual con 20 anos de experiencia."
>
> Con solo esta linea, Claude ajusta su vocabulario, nivel de detalle, formato de respuesta
> y enfoque general.

Pero los system prompts realmente poderosos van mucho mas alla de un rol simple.

---

### Estructura multi-seccion con XML

Para system prompts complejos, la mejor practica es dividirlo en **secciones logicas**
usando tags XML:

```xml
<rol>
Eres Sofia, asistente virtual de TechStore con 5 anos de experiencia
en atencion al cliente de productos electronicos.
</rol>

<instrucciones>
- Saluda al cliente por su nombre si lo proporciona
- Identifica el tipo de consulta antes de responder
- Ofrece siempre al menos dos opciones de solucion
</instrucciones>

<formato>
- Usa lenguaje amigable pero profesional
- Respuestas de maximo 150 palabras
- Incluye un numero de referencia con formato REF-XXXX
</formato>

<restricciones>
- NO compartas politicas internas de precios
- NO hagas promesas de reembolso sin verificar
- Si el tema no es de tecnologia, redirige amablemente
</restricciones>
```

Esta estructura le da a Claude instrucciones claras y organizadas que puede
seguir de manera consistente.

---

### Persona detallada

Un rol generico como "eres un experto" funciona, pero una **persona detallada**
produce resultados significativamente mejores:

- **Nombre y experiencia:** "Eres Dr. Martinez, cardiologo con 15 anos en el Hospital Central"
- **Estilo de comunicacion:** "Explicas conceptos complejos con analogias cotidianas"
- **Audiencia objetivo:** "Tu audiencia son pacientes sin formacion medica"

Mientras mas especifica sea la persona, mas consistente y natural sera
el comportamiento de Claude.

---

### Guardrails de comportamiento

Los guardrails son **restricciones activas** que definen:

- **Temas permitidos:** En que puede ayudar Claude
- **Temas prohibidos:** Que debe rechazar o redirigir
- **Como redirigir:** Que hacer cuando el usuario sale del tema

> **Ejemplo de guardrail:**
>
> "Si el usuario pregunta sobre temas que no sean de tu area de expertise,
> responde: 'Esa es una pregunta interesante, pero mi especialidad es [tema].
> Puedo ayudarte con algo relacionado a [tema]?'"

---

### Forzar formato de respuesta

El system prompt es el lugar ideal para forzar un **formato especifico** de respuesta:

- **JSON:** Para integracion con APIs y sistemas
- **XML:** Para respuestas estructuradas
- **Markdown:** Para documentacion
- **Formato personalizado:** Cualquier estructura que necesites

> **Ejemplo para forzar JSON:**
>
> "SIEMPRE responde en formato JSON valido con esta estructura exacta:
> `{"answer": "...", "confidence": "alta|media|baja", "sources_needed": true|false}`.
> Nunca respondas en texto plano."

---

### Mejores practicas

- **Longitud ideal:** Entre 500 y 2000 tokens. Suficiente para ser completo, no tanto como para diluir las instrucciones.
- **Instrucciones clave al inicio y al final:** Claude presta mas atencion al principio y al final del system prompt (efecto de primacia y recencia).
- **Ser explicito sobre lo que NO hacer:** Las restricciones son tan importantes como las instrucciones.
- **Probar con casos limite:** Un buen system prompt funciona bien no solo con el "camino feliz" sino tambien con entradas inesperadas.
""")

st.divider()
st.header("Ejercicios")

# ── Ejercicio 8.1 ──────────────────────────────────────────────
fields_system = [
    {"name": "SYSTEM_PROMPT", "label": "System Prompt", "rows": 8},
    {"name": "PROMPT", "label": "Mensaje del usuario", "rows": 3},
]

render_exercise(
    exercise_id="8.1",
    title="Bot de Atencion al Cliente",
    instruction="Escribe un system prompt multi-seccion para un bot de atencion al cliente que:\n\n1. **Categorice** el tipo de queja (envio, producto, facturacion, etc.)\n2. Muestre **empatia** hacia el cliente\n3. Proporcione un **numero de ticket o referencia**\n4. Estructure la respuesta con secciones claras\n\nPruebalo con el mensaje: *'Mi laptop no ha llegado despues de 3 semanas de espera.'*",
    hint="Usa secciones XML en tu system prompt: <rol>, <instrucciones>, <formato>. Incluye una instruccion explicita de generar un numero de referencia tipo REF-XXXX o TICKET-XXXX.",
    grade_fn=grade_8_1,
    fields=fields_system,
)

# ── Ejercicio 8.2 ──────────────────────────────────────────────
st.subheader("Ejercicio 8.2 - Guardrails Educativos")
st.markdown("""
Escribe un system prompt para un **tutor de matematicas** que:

- **Guie** al estudiante paso a paso sin dar respuestas directas
- **Rechace** temas que no sean de matematicas, redirigiendo amablemente

Se probara con **dos mensajes diferentes**. Ambos deben pasar para completar el ejercicio.
""")

system_8_2 = st.text_area(
    "System Prompt",
    height=200,
    key="sys_8_2",
)

if "8.2_math_passed" not in st.session_state:
    st.session_state["8.2_math_passed"] = False
if "8.2_off_passed" not in st.session_state:
    st.session_state["8.2_off_passed"] = False

col1, col2 = st.columns(2)
with col1:
    if st.button("Test: Pregunta matematica", key="run_8_2_math"):
        with st.spinner("Claude esta pensando..."):
            response = get_completion(
                "Cuanto es 15% de 80?", system_prompt=system_8_2
            )
        st.markdown("**Respuesta de Claude:**")
        st.code(response, language=None)
        if grade_8_2_math(response):
            st.success("Correcto! Claude guia sin dar la respuesta directa.")
            st.session_state["8.2_math_passed"] = True
        else:
            st.error("Claude no deberia dar la respuesta directa (12). Debe guiar al estudiante.")

with col2:
    if st.button("Test: Tema no permitido", key="run_8_2_off"):
        with st.spinner("Claude esta pensando..."):
            response = get_completion(
                "Cuentame sobre dinosaurios", system_prompt=system_8_2
            )
        st.markdown("**Respuesta de Claude:**")
        st.code(response, language=None)
        if grade_8_2_off(response):
            st.success("Correcto! Claude redirige al tema de matematicas.")
            st.session_state["8.2_off_passed"] = True
        else:
            st.error("Claude deberia redirigir al tema de matematicas, no responder sobre dinosaurios.")

if st.session_state.get("8.2_math_passed") and st.session_state.get("8.2_off_passed"):
    st.success("Ambos tests pasaron! Ejercicio completado.")
    st.session_state.completed.add("8.2")

if st.button("Ver pista", key="hint_8_2"):
    st.info(
        "Incluye restricciones claras en tu system prompt: "
        "'Solo responde preguntas de matematicas. Si el tema no es matematicas, "
        "redirige amablemente al estudiante. Nunca des la respuesta directa; "
        "en su lugar, haz preguntas que guien al estudiante hacia la solucion.'"
    )
st.divider()

# ── Ejercicio 8.3 ──────────────────────────────────────────────
render_exercise(
    exercise_id="8.3",
    title="Formato JSON Forzado",
    instruction='Escribe un system prompt que fuerce a Claude a **SIEMPRE** responder en formato JSON con esta estructura exacta:\n\n```json\n{"answer": "...", "confidence": "alta|media|baja", "sources_needed": true|false}\n```\n\nNo importa la pregunta del usuario, Claude debe responder en JSON valido con esas tres claves.\n\nPruebalo con cualquier pregunta, por ejemplo: *"Cual es la capital de Francia?"*',
    hint="Incluye un ejemplo del JSON esperado en tu system prompt y una instruccion explicita como 'SIEMPRE responde en JSON, sin excepciones. No agregues texto fuera del JSON.'",
    grade_fn=grade_8_3,
    fields=fields_system,
)
